from rest_framework import serializers
from .models import Network


class NetworkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['email']
