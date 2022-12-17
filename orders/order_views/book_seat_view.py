from orders.models import Order, OrderImage, Place
from orders.serializers import OrderSerializer, OrderImageSerializer, PlaceSerializer, OrderUpdateSerializer, BookSeatSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


class BookSeatView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSeatSerializer
    queryset = Order.objects.prefetch_related('images')
    permission_classes = [permissions.IsAuthenticated]
    

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        print(data)
        return data

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)