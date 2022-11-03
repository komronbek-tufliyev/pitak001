from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import (
    Order,
    OrderComment,
    OrderFile,
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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get']

class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get']

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    http_method_names = ['post']
    # parser_classes = (MultiPartParser, FormParser)

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # print(serializer.initial_data)
        # print(serializer.data)
        print("Requested data", request.data)
        # user = request.user
        # owner_id = user.id
        # request.data['owner'] = owner_id
        full_data = {
            'owner': '',
            'from_place': '',
            'to_place': '',
            'description': '',
            'images': '',
            'price': '',
            'car': '',
            'date': '',
            'car_number': '',
            'created_at': '',
            'updated_at': '',
            "is_active": True,
            "is_accepted": False,
            "is_finished": False,
            "is_canceled": False,
            "is_paid": False,
            "is_driver": False,
        }
        for key in full_data:
            if key in request.data:
                full_data[key] = request.data[key]

        print("Full data", full_data)

        context = {
            'request': request,
            'name': request.data['name'],
            'from_place': request.data['from_place'],
            'to_place': request.data['to_place'],
            'owner': request.user.id,
            # 'description': request.data['description'],
            'price': request.data['price'],
            'date': request.data['date'],
            'car': request.data['car'],
            'car_number': request.data['car_number'],
            # 'is_driver': request.data['is_driver'],
            # 'is_active': request.data['is_active'],
            # 'is_finished': request.data['is_finished'],
            # 'is_canceled': request.data['is_canceled'],
            # 'is_paid': request.data['is_paid'],
            # 'is_accepted': request.data['is_accepted'],
            # 'created_at': request.data['created_at'],
            # 'updated_at': request.data['updated_at'],
            'images': request.data['images'],

        }

        context_p = {
            # 'request': request,
            'owner': request.user.id,
            # 'validated_data': request.data,
            **request.data
        }
        print("Context", context_p)
        serializer = self.get_serializer(data=full_data)
        # print("\n\n\nContext", context)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print("Serialized data", serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    