from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.

class Location(models.Model):
    locationID = models.UUIDField("Location ID",primary_key=True,max_length=48,default=uuid4)
    coordinates = models.CharField("Coordinates", max_length=50,unique=True)
    city = models.CharField(max_length=80,blank=True)
    state = models.CharField(max_length=80,blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.coordinates


class Client(models.Model):
    clientID = models.UUIDField("Client ID",primary_key=True,max_length=48,default=uuid4)
    name = models.CharField("Client Name",max_length=35)
    email = models.EmailField("Client Email",unique=True)
    auth_user = models.OneToOneField(User,related_name='client',on_delete=models.PROTECT)
    mobile = models.BigIntegerField("Phone number",validators=[
        MaxValueValidator(9999999999,"Please provide a valid mobile number"),
        MinValueValidator(1111111111,"Please provide a valid mobile number")
    ])

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"


class ClientLocation(models.Model):
    client = models.ForeignKey(Client,related_name="locations",on_delete=models.CASCADE)
    location = models.ForeignKey(Location,related_name="clients",on_delete=models.CASCADE)
    alias = models.CharField("Location name for client",max_length=20,default="Others")
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.client} - {self.alias}"