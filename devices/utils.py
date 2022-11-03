from .models import Device, DeviceToken
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

def get_device_type(request):
    return request.data['device_type']

def get_device_id(request):
    return request.data['device_id']

def get_app_version(request):
    return request.data['app_version']

def get_device_token(request):
    return request.data['device_token']

def get_device_name(request):
    return request.data['device_name']

def get_device_status(request):
    return request.data['device_status']
    
def get_device_token_status(request):
    return request.data['is_active']

def get_device_token(request):
    return request.data['token']

