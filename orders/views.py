from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import (
    Order,
    OrderComment,
    OrderImage,
    Place,
)

from .serializers import (
    OrderSerializer,
    OrderCommentSerializer,
    CreateOrderSerializer,
    PlaceSerializer,
)

User = get_user_model()

class OrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('images')
    serializer_class = OrderSerializer
    http_method_names = ['get']

class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.prefetch_related('images')
    serializer_class = OrderSerializer(queryset, many=True)
    http_method_names = ['get']

class OrderCreateView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    http_method_names = ['post']
    # parser_classes = (MultiPartParser, FormParser)

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # full_data = {
        #     'owner': '',
        #     'from_place': '',
        #     'to_place': '',
        #     'description': '',
        #     'images': '',
        #     'uploaded_images': '',
        #     'price': '',
        #     'car': '',
        #     'date': '',
        #     'car_number': '',
        #     'created_at': '',
        #     'updated_at': '',
        #     "is_active": True,
        #     "is_accepted": False,
        #     "is_finished": False,
        #     "is_canceled": False,
        #     "is_paid": False,
        #     "is_driver": False,
        # }
        # for key in full_data:
        #     if key in request.data:
        #         full_data[key] = request.data[key]
      
        # full_data['owner'] = request.user.id
        # print("Full data", request.data)
        serializer = CreateOrderSerializer(data=request.data, context={'owner': request.user})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'detail':serializer.data, 'status': True}, status=status.HTTP_201_CREATED)
        # headers = self.get_success_headers(serializer.data)
        return Response({'detail': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)
class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['put']

    permission_classes = [permissions.IsAuthenticated]

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['delete']

    permission_classes = [permissions.IsAuthenticated]

class OrderCommentList(generics.ListAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['get']

class OrderCommentDetail(generics.RetrieveAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['get']

class OrderCommentCreateView(generics.CreateAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['post']

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderCommentUpdateView(generics.UpdateAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['put', 'patch']

    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderCommentDeleteView(generics.DestroyAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['delete']

    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlaceList(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    http_method_names = ['get']


class PlaceDetail(generics.RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    http_method_names = ['get']

class PlaceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlaceSerializer)
    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    