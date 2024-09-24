from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from network.models import Network, Person
from network.serializers import NetworkCreateSerializer, PersonRetrieveListSerializer

from linkedin_scraper import LinkedinScraper
from network.services.profile_parser import ProfileParser

class NetworkViewSet(CreateModelMixin, GenericViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkCreateSerializer


@api_view(['GET', 'POST'])
def person_view(request):
    # Get network authorization
    network = get_network_from_headers(request)
    if not network:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return handle_get_request(network)

    if request.method == 'POST':
        return handle_post_request(request, network)


def get_network_from_headers(request):
    slug = request.headers.get('Network-Identifier', None)
    if slug:
        return Network.objects.filter(slug=slug).first()
    return None


def handle_get_request(network):
    persons = Person.objects.filter(networks=network)
    serializer = PersonRetrieveListSerializer(persons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def handle_post_request(request, network):
    linkedin_identifier = request.data.get('linkedin_identifier', None)
    if not linkedin_identifier:
        return Response({'error': 'linkedin_identifier is required'}, status=status.HTTP_400_BAD_REQUEST)

    identifier_from_url = extract_identifier_from_url(linkedin_identifier)

    person = get_person_or_ingest(identifier_from_url)
    if not person:
        return Response({'error': 'Unable to create person'}, status=status.HTTP_400_BAD_REQUEST)

    person.networks.add(network)
    person.save()

    serializer = PersonRetrieveListSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)


def extract_identifier_from_url(linkedin_identifier):
    return linkedin_identifier.strip('/').split('/')[-1].split('?')[0]


def get_person_or_ingest(identifier_from_url):
    person = Person.objects.filter(linkedin_identifier=identifier_from_url).first()
    if not person:
        profile_data = LinkedinScraper.get_profile(f'https://www.linkedin.com/in/{identifier_from_url}')
        ProfileParser.ingest_profile_data(profile_data)
        person = Person.objects.filter(linkedin_identifier=identifier_from_url).first()
    return person
