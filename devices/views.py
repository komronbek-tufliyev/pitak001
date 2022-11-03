from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .serializers import DeviceSerializer, DeviceTokenSerializer
from .models import Device, DeviceToken
from .utils import get_device_type, get_app_version, get_device_token, get_device_name, get_device_status, get_device_token_status, get_device_token



class DeviceView(generics.CreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        device_type = get_device_type(request)
        app_version = get_app_version(request)
        device_token = get_device_token(request)
        device_name = get_device_name(request)
        device_status = get_device_status(request)
        user = request.user
        device = Device.objects.create(device_type=device_type, app_version=app_version, device_token=device_token, device_name=device_name, device_status=device_status, user=user)
        device.save()
        return Response({'message': _('Device created successfully')}, status=status.HTTP_201_CREATED)

class DevicesView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)