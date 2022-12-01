from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.pagination import PageNumberPagination
# imort login_required
from django.contrib.auth.decorators import login_required
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
    DisplayFavOrderSerializer,
    OrderUpdateSerializer,
    CreateOrderDisplaySerializer,
    FilterByPlaceSerializer,
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
    serializer_class = OrderSerializer
    http_method_names = ['get']

class OrderCreateView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    http_method_names = ['post']
    # parser_classes = (MultiPartParser, FormParser)

    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(request_body=CreateOrderDisplaySerializer)
    def create(self, request, *args, **kwargs):
        if 'to_place' in request.data and 'to_place_district' in request.data:
            to_place_region = request.data.get('to_place', None)
            to_place_district = request.data.get('to_place_district', None)
            # print("to_place", to_place)
            # print("to_place_district", to_place_district)
            # if not to_place and to_place_district:
            #     msg = {'detail': 'to_place is required'}
            # elif not to_place_district and to_place:
            #     msg = {'detail': 'to_place_district is required'}
            # elif not to_place and not to_place_district:
            #     msg = {'detail': 'to_place and to_place_district is required'}
            # if to_place and to_place_district:

            to_place_id = Place.objects.filter(region=to_place_region, district=to_place_district)
            if to_place_id.exists():
                to_place = to_place_id.first().pk
            else:
                return Response({'detail': f'Bunday id-ga ega manzil topilmadi, id: yo\'q chunki manzilni o\'zi yo\'q'}, status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     to_place = Place.objects.create(region=to_place_region, district=to_place_district).pk
            
            request.POST._mutable = True
            request.data['to_place'] = to_place
            request.POST._mutable = False
            serializer = CreateOrderSerializer(data=request.data, context={'owner': request.user})

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                print("ser data", serializer.data)
                return Response({'detail':serializer.data, 'status': True}, status=status.HTTP_201_CREATED)
            # headers = self.get_success_headers(serializer.data)
            return Response({'detail': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'to_place and to_place_district are required'}, status=status.HTTP_400_BAD_REQUEST)



class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.prefetch_related('images')
    serializer_class = OrderSerializer
    http_method_names = ['put', 'patch']
    lookup_field = 'pk'

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CreateOrderDisplaySerializer)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        phone2 = request.data.get('phone2', None)
        if phone2:
            request.data['phone2'] = phone2.replace('+', '')
        to_place_region = request.data.get('to_place', None)
        to_place_district = request.data.get('to_place_district', None)
        if to_place_region and to_place_district:
            to_place_id = Place.objects.filter(region=to_place_region, district=to_place_district)
            if to_place_id.exists():
                to_place = to_place_id.first().pk
                request.POST._mutable = True
                request.data['to_place'] = to_place
                request.POST._mutable = False
            else:
                return Response({'status': False, 'detail': f'Bunday manzil topilmadi, To place exists: {to_place_id.exists()}'}, status=status.HTTP_400_BAD_REQUEST)
        # if to_place_region and to_place_district:
        #     to_place_id = Place.objects.filter(region=to_place_region, district=to_place_district)
        #     if to_place_id.exists():
        #         to_place = to_place_id.first().pk
        #     else:
        #         to_place = Place.objects.create(region=to_place_region, district=to_place_district).pk
        #     request.POST._mutable = True
        #     request.data['to_place'] = to_place
        #     request.POST._mutable = False
        # elif to_place_region and not to_place_district:
        #     return Response({'detail': 'to_place_district is required'}, status=status.HTTP_400_BAD_REQUEST)
        # elif not to_place_region and to_place_district:
        #     to_place_id = Place.objects.filter(district=to_place_district, region=instance.to_place.region)
        #     if to_place_id.exists():
        #         to_place = to_place_id.first().pk
        #     else:
        #         to_place = Place.objects.create(region=instance.to_place.region, district=to_place_district).pk
        #   request.POST._mutable = True
        #   request.data['to_place'] = to_place
        #   request.POST._mutable = False
        
        serializer = OrderUpdateSerializer(instance=instance, data=request.data, context={'owner': request.user},  partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'detail':serializer.data, 'status': True, 'message': 'Order updated succesfully'}, status=status.HTTP_201_CREATED)
        # headers = self.get_success_headers(serializer.data)
        return Response({'detail': serializer.errors, 'status': False, 'message': 'Could not update order'}, status=status.HTTP_400_BAD_REQUEST)

        

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['delete']

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({'detail': 'Order deleted succesfully'}, status=status.HTTP_200_OK) 

class OrderCommentList(generics.ListAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['get']
    pagination_class = MyPagination

class OrderCommentDetail(generics.RetrieveAPIView):
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

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
    # def get(self, request, format=None):
    #     places = Place.objects.all()
    #     serializer = PlaceSerializer(places, many=True)
    #     return Response(serializer.data)

    @swagger_auto_schema(request_body=PlaceSerializer)
    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilterByRegionView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super().get_queryset()
        region_by = self.kwargs['region']
        if region_by:
            queryset =  Place.objects.filter(region=region_by).all()
        return queryset

class FavOrderView(APIView):
    """
        Favourite Order View has two methods: post and delete
        # Post method addes user id to order.favourite m2m field
        # Delete method removes user id from order.favourite m2m field 
    """
    def get(self, request):
        user = request.user
        print("fav orders", user)
        try:

            serializer = FavouriteOrderSerializer(user)
            return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error", e)
            return Response({'status': False, 'detail': f"Error {e}"}, status=status.HTTP_204_NO_CONTENT)
   
    @swagger_auto_schema(request_body=DisplayFavOrderSerializer)
    def post(self, request):
        if 'id' in request.data:
            order = get_object_or_404(Order, id=request.data.get('id'))
            user = request.user
            print("User", user)
            print("User fav", user.favourite.all())
            print("Order", order)
            print("is Order in user.fav ", order in user.favourite.all())
            if order in user.favourite.all():
                return Response({'status': False, 'detail': 'Order already in favourite'}, status=status.HTTP_200_OK)   
            serializer = FavouriteOrderSerializer(data=request.data, context={'user': user, 'order': order})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'status': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
           
        print("Anaqa...", "error chiqdi bro")    
        return Response({'status': False, 'message': 'E karochi xatolik borde, kodingni to\'g\'irla keyin ishlayman'})
    
    @swagger_auto_schema(request_body=DisplayFavOrderSerializer)
    def delete(self, request):
        if 'id' in request.data:
            user = request.user
            order = get_object_or_404(Order, id=request.data.get('id'))
            if order and order in user.favourite.all():
                user.favourite.remove(order)
                user.save()
                return Response({'status': True, 'detail': 'Order succesfully removed from favourites'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'detail': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'status': False, 'detail': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)
        print("Aka xatolik chiqdi qanday aytay")

        return Response({'status': False, 'detail': 'E karochi xatolik borde, kodingni to\'g\'irla keyin ishlayman'})



class MyOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = MyPagination
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('images').prefetch_related('to_place')

        user = self.request.user 
        if user is not None:
            queryset = queryset.filter(owner=user)
        return queryset

class Orders4DriverView(generics.ListAPIView):
    # queryset = Order.objects.all()
    pagination_class = MyPagination
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('images').prefetch_related('to_place').filter(is_driver=False)
        return queryset

class Orders4NonDriverView(generics.ListAPIView):
    # queryset = Order.objects.all()
    pagination_class = MyPagination
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('images').prefetch_related('to_place').filter(is_driver=True)
        return queryset

class FilteredOrders4DriverView(generics.ListAPIView):
    queryset = Order.objects.all()
    pagination_class = MyPagination
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        to_place_district = self.kwargs.get('to_place_district', None)
        to_place_region = self.kwargs.get('to_place_region', None)
        from_place = self.kwargs.get('from_place', None)
        if to_place_region and from_place and to_place_district:
            if to_place_region and from_place and to_place_district:
                to_place_id = Place.objects.filter(region=to_place_region).filter(district=to_place_district)
                if to_place_id.exists():
                    to_place_id = to_place_id.first()
                    
                    queryset = Order.objects.filter(is_driver=False).filter(from_place=from_place, to_place=to_place_id).prefetch_related('images').prefetch_related('to_place') 

        return queryset


class FilteredOrders4NonDriverView(generics.ListAPIView):
    queryset = Order.objects.all()
    pagination_class = MyPagination
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        to_place_district = self.kwargs.get('to_place_district', None)
        to_place_region = self.kwargs.get('to_place_region', None)
        from_place = self.kwargs.get('from_place', None)
        if to_place_region and from_place and to_place_district:
            if to_place_region and from_place and to_place_district:
                to_place_id = Place.objects.filter(region=to_place_region).filter(district=to_place_district)
                if to_place_id.exists():
                    to_place_id = to_place_id.first()
                    
                    queryset = Order.objects.filter(is_driver=True).filter(from_place=from_place, to_place=to_place_id).prefetch_related('images').prefetch_related('to_place') 

        return queryset