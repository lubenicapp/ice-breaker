from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from network.models import Network, Person
from network.serializers import NetworkCreateSerializer, PersonRetrieveListSerializer


class NetworkViewSet(CreateModelMixin, GenericViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkCreateSerializer


@api_view(['GET', 'POST'])
def person_view(request):
    slug = request.headers.get('Network-Identifier', None)
    network = Network.objects.filter(slug=slug).first()
    if not slug or not network:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        persons = Person.objects.filter(networks=network)
        serializer = PersonRetrieveListSerializer(persons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        linkedin_identifier = request.data.get('linkedin_identifier', None)
        if not linkedin_identifier:
            return Response({'error': 'linkedin_identifier is required'}, status=status.HTTP_400_BAD_REQUEST)

        person, _ = Person.objects.get_or_create(linkedin_identifier=linkedin_identifier)
        person.networks.add(network)
        person.save()
        serializer = PersonRetrieveListSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)
