from .models import Device, DeviceToken
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

# Connected devices model
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        
    def create(self, validated_data):
        if Device.objects.filter(device_id=validated_data['device_id']).exists():
            device = Device.objects.get(device_id=validated_data['device_id'])
            device.device_status = validated_data['device_status']
            device.save()
            return device
        else:
            return Device.objects.create(**validated_data)

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = '__all__'
        
    def create(self, validated_data):
        if DeviceToken.objects.filter(token=validated_data['token']).exists():
            device_token = DeviceToken.objects.get(token=validated_data['token'])
            device_token.is_active = validated_data['is_active']
            device_token.save()
            return device_token
        else:
            return DeviceToken.objects.create(**validated_data)