from rest_framework import serializers
from django.db import transaction
from .models import *

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('coordinates','city','state','address')

class ClientSerializer(serializers.ModelSerializer):

    location = LocationSerializer()
    username = serializers.CharField(allow_blank = True)
    password = serializers.CharField(allow_blank = True)


    class Meta:
        model = Client
        depth = 1
        fields = ('name','email','username','password','mobile','location')
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                auth_user = User.objects.create_user(username=validated_data.pop("username"),password=validated_data.pop("password"),email=validated_data.get("email"))
                location = validated_data.pop('location')
                loc,created = Location.objects.get_or_create(**location)
                print(loc)
                print(validated_data)
                client = Client.objects.create(**validated_data,auth_user=auth_user)
                cl = ClientLocation.objects.create(client=client,location=loc)
                return client
        except Exception as e:
            raise serializers.ValidationError(e)