from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.pagination import PageNumberPagination
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
    FavouriteOrderSerializer,
)

User = get_user_model()

class MyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('images')
    serializer_class = OrderSerializer
    http_method_names = ['get']
    pagination_class = MyPagination

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
    pagination_class = MyPagination

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

 
class FavOrderView(APIView):
    """
        Favourite Order View has two methods: post and delete
        # Post method addes user id to order.favourite m2m field
        # Delete method removes user id from order.favourite m2m field 
    """
    def get(self, request):
        user = request.user
        queryset = User.objects.all()
        print("fav orders", queryset)
        try:

            serializer = FavouriteOrderSerializer(queryset, many=True)
            # if serializer.is_valid(raise_exception=True):
            return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_200_OK)
            # return Response({'status': False, 'detail': serializer.errors}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print("Error", e)
            return Response({'status': False, 'detail': f"Error {e}"}, status=status.HTTP_204_NO_CONTENT)
        # return Response({}) 

    def post(self, request):
        if 'order' in request.data:
            order = get_object_or_404(Order, id=request.data.get('order'))
            user = request.user
            print("User", user)
            print("User fav", user.favourite.all())
            print("Order", order)
            print("is Order in user.fav ", order in user.favourite.all())
            if order and order not in user.favourite.all():
                user.favourite.add(order)
                return Response({'status': True, 'deatil': 'Order added to favourites'}, status=status.HTTP_201_CREATED)
            print("Anaqa...", "error chiqdi bro")    
        return Response({'status': False, 'detail': 'Something went wrong'})

    def delete(self, request):
        if 'order' in request.data:
            user = request.user
            order = get_object_or_404(Order, id=request.data.get('order'))
            if order and order in user.favourites.all():
                user.favourite.remove(order)
                return Response({'status': True, 'detail': 'Order succesfully removed from favourites'}, status=status.HTTP_200_OK)

            print("Aka xatolik chiqdi qanday aytay")

        return Response({'status': False, 'detail': 'E karochi xatolik borde, kodingni to\'g\'irla keyin ishlayman'})



