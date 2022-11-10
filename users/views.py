from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.views import APIView

from .serializers import (
    UserSerializer, 
    ValidateSendOTPSerializer, 
    ValidateOTPSerializer, 
    CreateUserSerializer, 
    LoginSerializer,
    MyTokenObtainPairSerializer,
    LogoutSerializer,
    UpdateUserSerializer,
    
)
from .models import PhoneOTP, User
from .utils import send_sms

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from drf_yasg import openapi

class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()

# class UserView(generics.RetrieveAPIView):
#     permission_classes = (permissions.IsAuthenticated,  )
#     serializer_class = UserSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

     
class ValidateOTPView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = ValidateOTPSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=ValidateOTPSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ValidateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get('phone')
        otp = serializer.data.get('otp')
        if phone and otp:
            phone = phone.replace('+', '')
            phoneotp = PhoneOTP.objects.filter(phone=phone)
            user = User.objects.filter(phone=phone)
            if not user.exists():
                phoneotp = phoneotp.first()
                user = user.first()
                if phoneotp.otp == otp:
                    phoneotp.is_verified = True
                    phoneotp.save()
                    return Response({'message': 'OTP verified succesfully. Now you can register/login phone'}, status=status.HTTP_200_OK)
 
            if phoneotp.exists() and user.exists():
                phoneotp = phoneotp.first()
                user = user.first()
                if phoneotp.otp == otp:
                    phoneotp.is_verified = True
                    phoneotp.save()

                    user.set_password(otp)
                    user.save()
                    return Response({'message': 'OTP verified succesfully. Now you can register/login phone'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "Something went wrong while validating otp"}, status=status.HTTP_102_PROCESSING)
        else:
            return Response({'message': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = ValidateSendOTPSerializer
    http_method_names = ['post']

    send_otp_response = openapi.Response('response description', ValidateSendOTPSerializer)
    send_otp_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='boolean'),
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        },
    )

    @swagger_auto_schema(request_body=ValidateSendOTPSerializer, responses={200: send_otp_response}, response_body=send_otp_schema, )
    def post(self, request, *args, **kwargs):
        serializer = ValidateSendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get('phone')
        try:
            print(phone, "Phone edi")
            phone = phone.replace('+', '')
            print("Phone esa ", phone)
            key = send_sms(phone)
            print("Key: ", key)
            phone_otp = PhoneOTP.objects.filter(phone=phone)
            if phone_otp.exists():
                print("Phone otp exists and phone is", phone_otp)
                phone_otp = phone_otp.first()
                phone_otp.otp = key
                phone_otp.is_verified = False
                phone_otp.save()

            else:
                print("No phoneotp exists")
                phone_otp = PhoneOTP.objects.create(phone=phone, otp=key)
            return Response({'message': 'OTP sent succesfully'}, status=status.HTTP_200_OK)

            # phoneotp = PhoneOTP.objects.create(phone=phone, otp=key)
            # phoneotp.save()
            # return Response({'message': 'OTP sent succesfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Error sending OTP'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CreateUserSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=CreateUserSerializer)
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        if phone and password:
            phone = phone.replace('+', '')
            phoneotp = PhoneOTP.objects.filter(phone=phone)
            if phoneotp.exists():
                phoneotp = phoneotp.first()
                if phoneotp.is_verified:
                    request.data._mutable=True 
                    request.data['phone'] = phone
                    request.data._mutable = False
                    serializer = CreateUserSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    return Response({'message': 'User registered succesfully',}, status=status.HTTP_201_CREATED)

                else:
                    return Response({'message': 'Please verify OTP first'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Please verify OTP first'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Phone and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'message': 'User already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        phone = request.data.get('phone')
        password = request.data.get('password')
        refresh_token = request.GET.get('refresh')
        if phone and password:
            phone = phone.replace('+', '')
            phoneotp = PhoneOTP.objects.filter(phone=phone)
            if phoneotp.exists():
                phoneotp = phoneotp.first()
                if phoneotp.is_verified:
                    user = User.objects.filter(phone=phone)
                    if user.exists():
                        user = user.first()
                        print("User exists", user)
                        print("User checked_password = ", user.check_password(password))
                        # if not refresh_token:
                        #     refresh_token = RefreshToken()
                        # request.data._mutable = True
                        # request.data['refresh'] = refresh_token
                        # request.data._mutable = False
                        # serializer = LoginSerializer(data=request.data)
                        # serializer.is_valid(raise_exception=True)
                        # token = get_tokens_for_user(user)
                        if user.check_password(password):
                            token = get_tokens_for_user(user)
                            return Response({'message': 'User logged in succesfully', 'token': token}, status=status.HTTP_200_OK)
                        else:
                            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'Please verify OTP first'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Please verify OTP first'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Phone and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(request_body=LoginSerializer)
    # def post(self, request, *args, **kwargs):
    #     serializer = LoginSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     phone = serializer.data.get('phone')
    #     password = serializer.data.get('password')
    #     user = User.objects.get(phone=phone)
    #     if user.check_password(password):
    #         token = get_tokens_for_user(user)
    #         return Response({'message': 'User logged in succesfully', 'token': token}, status=status.HTTP_200_OK)
    #         # return Response({'message': 'User logged in succesfully'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

               

# Path: users\serializers.py
# Compare this snippet from users\models.py:
#

class UsersListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,  )
    serializer_class = UserSerializer
    queryset = User.objects.all()   
    http_method_names = ['get']
    pagination_class = MyPagination


class UserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,  )
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


    def get_object(self):
        return self.request.user

class UpdateUserView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,  )
    serializer_class = UpdateUserSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user

    


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,  )
    serializer_class = UserSerializer
    http_method_names = ['delete']

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)    


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,  )
    serializer_class = UserSerializer
    http_method_names = ['delete']

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LogoutSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User logged out succesfully'}, status=status.HTTP_200_OK)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class APILogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})
