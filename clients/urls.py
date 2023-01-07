from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/',ClientRegisterAPI.as_view()),
    path('add/location/',AddClientLocation.as_view()),
    path('login/',ClientLoginAPI.as_view())

]
