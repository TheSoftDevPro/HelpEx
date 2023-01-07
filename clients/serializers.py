from rest_framework import serializers
from django.db import transaction
from .models import *

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('coordinates','city','state','address')
        extra_kwargs = {
            'coordinates': {
                'validators' : []
            }
        }

class ClientSerializer(serializers.ModelSerializer):

    location = LocationSerializer(write_only = True)
    username = serializers.CharField(allow_blank = False,write_only = True)
    password = serializers.CharField(allow_blank = False,write_only = True)


    class Meta:
        model = Client
        depth = 1
        fields = ('name','email','username','password','mobile','location')
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                auth_user = User.objects.create_user(username=validated_data.pop("username"),password=validated_data.pop("password"),email=validated_data.get("email"))
                location = validated_data.pop('location')
                loc,created = Location.objects.get_or_create(coordinates = location.pop('coordinates'))
                # loc.
                client = Client.objects.create(**validated_data,auth_user=auth_user)
                cl = ClientLocation.objects.create(client=client,location=loc)
                print("created")
                return client
        except Exception as e:
            raise serializers.ValidationError(e)

class ClientLocationSerializer(serializers.ModelSerializer):

    loc = LocationSerializer()

    class Meta:
        model = ClientLocation
        depth = 1
        fields = ('loc','alias','is_default')
    
    def create(self, validated_data):
        location = validated_data.pop('loc')
        loc,created = Location.objects.get_or_create(coordinates = location.pop('coordinates'))
        print(self.context)
        cl,created = ClientLocation.objects.get_or_create(client = self.context.get('client'),location = loc)
        cl.alias = validated_data.get('alias')
        cl.is_default  = validated_data.get('is_default')
        cl.save()
        if not created:
            raise serializers.ValidationError({"message":"Address already added"})
        return cl
