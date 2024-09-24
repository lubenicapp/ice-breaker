from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from network.models import Network
from network.serializers import NetworkCreateSerializer


class NetworkViewSet(CreateModelMixin, GenericViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkCreateSerializer
