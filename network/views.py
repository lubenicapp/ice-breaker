from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from network.models import (
    Network,
    Person,
    Company,
    School,
    WorkExperience,
    EducationExperience,
)
from network.serializers import (
    NetworkCreateSerializer,
    PersonRetrieveListSerializer,
)

from linkedin_scraper import LinkedinScraper
from network.services.profile_parser import ProfileParser


class NetworkViewSet(CreateModelMixin, GenericViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkCreateSerializer


@api_view(['GET'])
def me(request):
    network = _get_network_from_headers(request)
    if not network:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(
        {'email': network.email, 'name': network.name},
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
def graph(request):
    network = _get_network_from_headers(request)
    if not network:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


    persons = Person.objects.filter(networks=network)
    companies = Company.objects.filter(work_experiences__person__in=persons)
    schools = School.objects.filter(education_experiences__person__in=persons)

    nodes = [p.as_node for p in persons] + [c.as_node for c in companies] + [s.as_node for s in schools]

    links = (
        [w.as_link for w in WorkExperience.objects.all(person__in=persons)]
        + [s.as_link for s in EducationExperience.objects.all(person__in=persons)]
    )

    return Response({'nodes': nodes, 'links': links}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def person_view(request):
    network = _get_network_from_headers(request)
    if not network:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        persons = Person.objects.filter(networks=network).prefetch_related(
            'work_experiences', 'education_experiences'
        )
        serializer = PersonRetrieveListSerializer(persons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        linkedin_identifier = request.data.get('linkedin_identifier', None)
        if not linkedin_identifier:
            return Response(
                {'error': 'linkedin_identifier is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        identifier_from_url = _extract_identifier_from_url(linkedin_identifier)

        try:
            person = _get_person_or_ingest(identifier_from_url)
            if not person:
                raise ValueError('Unable to create entity')
        except (Exception, ValueError):
            return Response(
                {'error': 'Unable to create entity'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        person.networks.add(network)
        person.save()

        serializer = PersonRetrieveListSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)


def _get_network_from_headers(request):
    slug = request.headers.get('Network-Identifier', None)
    if slug:
        return Network.objects.filter(slug=slug).first()
    return None


def _extract_identifier_from_url(linkedin_identifier):
    return linkedin_identifier.strip('/').split('/')[-1].split('?')[0]


def _get_person_or_ingest(identifier_from_url):
    person = Person.objects.filter(
        linkedin_identifier=identifier_from_url
    ).first()
    if not person:
        profile_data = LinkedinScraper.get_profile(
            f'https://www.linkedin.com/in/{identifier_from_url}'
        )
        person = ProfileParser.ingest_profile_data(profile_data)
    return person
