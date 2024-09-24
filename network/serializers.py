from rest_framework import serializers
from .models import Network, Person


class NetworkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['email']

class PersonRetrieveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['linkedin_identifier', 'first_name', 'last_name', 'profile_picture_url', 'skills']

class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['linkedin_identifier']
