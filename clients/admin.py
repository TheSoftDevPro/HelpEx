from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('coordinates','city','state')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name','email')

@admin.register(ClientLocation)
class ClientLocationAdmin(admin.ModelAdmin):
    list_display = ('client','alias','is_default')

