from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import (
    PhoneOTP, 
    User,
    Device,
)


User = get_user_model()


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'phone2', 'name', 'password', 'image', 'is_active', 'is_driver', 'devices', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError('Password is required')
        return password
    
    def validate_phone(self, phone):
        if not phone:
            raise serializers.ValidationError('Phone is required')
        return phone

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['phone', 'phone2', 'name']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'phone2', 'name', 'password', 'is_active', 'is_driver', 'image')
        extra_kwargs = {
            'password': {'write_only': True}
        }    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_driver = validated_data.get('is_driver', instance.is_driver)
        instance.image = validated_data.get('image', instance.image)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.phone2 = validated_data.get('phone2', instance.phone2)
        instance.save()
        
        return instance


class ValidateSendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, allow_null=False, min_length=12, help_text=_("Telefon raqam: 998XX123ZZYY"))
    def validate_phone(self, phone):
        if not phone:
            raise serializers.ValidationError('Phone number is required')
        
        return phone
    def to_representation(self, instance):
        data = super().to_representation(instance)
        print("Data respresentation", data)
        data.update({'detail': 'Otp sent succesfully'})
        return data

class ValidateOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, help_text=_("Telefon raqam: 998XX123ZZYY"), allow_null=False)
    otp = serializers.CharField(max_length=4, min_length=4, help_text=_("Bir martalik yuborilgan kodd"), allow_null=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp = attrs.get('otp')
        if not phone:
            raise serializers.ValidationError('Phone number is required')
        if not otp:
            raise serializers.ValidationError('OTP is required')
        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['phone'] = user.phone
        token['phone2'] = user.phone2
        token['image'] = user.image
        token['is_driver'] = user.is_driver
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        token['is_superuser'] = user.is_superuser
        return token


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['name', 'phone', 'phone2', 'image', 'is_driver']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_phone(self, phone):
        if not phone:
            raise serializers.ValidationError('Phone is required')
        return phone


    def validate(self, attrs):
        print("Attrs", attrs)
        phone = attrs.get('phone')
        if phone:
            phone = phone.replace('+', '')
            user = User.objects.filter(phone=phone)
            if user.exists():
                print("User exists")
                raise serializers.ValidationError('User already exists')
            return attrs
        
        else:            
            raise serializers.ValidationError('Phone are required')
    
 
    
    def create(self, validated_data):
        try:
            self.validate(validated_data)
            print("Val data", validated_data)
            phone = validated_data.pop('phone').replace('+', '')
            print("Serializerdagi tel", phone)
            phone2 = validated_data.pop('phone2', None)
            if phone2:
                phone2 = phone2.replace('+', '')
            image = validated_data.pop('image', None)
            is_driver = validated_data.pop('is_driver', False)
            phoneotp = PhoneOTP.objects.filter(phone=phone)
            name = validated_data.get('name', None)
            if phoneotp.exists():
                password = phoneotp.first().otp
                if '+' in phone:
                    phone = phone.replace('+', '')
                user = User.objects.create(phone=phone, password=password, phone2=phone2, image=image, is_driver=is_driver, name=name)
                print("Usr created da aka")
                user.set_password(password)
                user.save()
                print("User: ", user, user.password)
            else:
                raise serializers.ValidationError("Can not create user, because phoneotp does not exist")
            print("validated")
            return user
        except Exception as e:
            print("Error in create: ", e)
            raise serializers.ValidationError('User already exists')

        # return user 

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=12, max_length=13, help_text=_("Telefon raqam: 998XX123ZZYY"))
    password = serializers.CharField(min_length=4, max_length=4, help_text=_("Parol. Bir martalik tasdiqlangan/yuborilgan kod"))
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired'),
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

            