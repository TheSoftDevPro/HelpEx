from rest_framework.viewsets import ViewSet
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.
from .serializers import *
from .models import *

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from core.auth import ClientAuthentication
from core.encryption import raw_to_encrypted as encrypt

class ClientRegisterAPI(GenericAPIView):

    authentication_classes = []
    serializer_class = ClientSerializer

    def post(self,request):

        """
        INPUT:
        {
            "name":"John Doe",
            "email":"john@doe.com",
            "username":"jd",
            "password":"doe@JOHN",
            "mobile":8989898989,
            "location":{
                "coordinates":"00.00,00.00",
                "city":"JDCITY", // Not required
                "state":"JDSTATE", // Not required
                "address":"12,JDStreet,JDCITY" // Not required
            }
        }
        """
        data  = request.data
        serializer = ClientSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Registered Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class ClientLoginAPI(APIView):

    authentication_classes = []

    def post(self,request):

        """
        INPUT:
        {
            "username":"jd",
            "password":"doe@JOHN"
        }
        """

        data = request.data
        username = data.get("username",None)
        password = data.get("password",None)
        user = None
        if username is None or password is None:
            return Response({"message":"Username or Password missing"},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username,password=password)
        if user is None:
            return Response({"message":"Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)
        try:
            Client.objects.get(auth_user=user)
        except:
            return Response({"message":"User does not exist! Please Sign Up"},status=status.HTTP_400_BAD_REQUEST)
        token,created = Token.objects.get_or_create(user = user)
        return Response({"token":encrypt(token.key)},status=status.HTTP_202_ACCEPTED)

class AddClientLocation(GenericAPIView):
    
    authentication_classes = [ClientAuthentication]
    serializer_class = ClientLocationSerializer


    def post(self,request):
        data  = request.data
        serializer = self.serializer_class(data = data,context = {"client":request.user.client})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"New address added"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    