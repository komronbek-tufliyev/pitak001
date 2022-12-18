from orders.models import Order, OrderImage, Place
from orders.serializers import BookSeatSerializer, SeatSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

class BookaSet(generics.CreateAPIView):
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order', None)
        if order_id is not None:
            order =  Order.objects.filter(pk=order_id)
            if order.exists():
                order = order.first()
                serializer = SeatSerializer(data=request.data, context={'request': request, 'order': order})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return  Response({'status': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': False, 'detail': 'Bunday order topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": False, 'detail': 'Nimadur xato ketdi'}, status=status.HTTP_400_BAD_REQUEST)

# class BookSeatView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SeatSerializer
    queryset = Order.objects.prefetch_related('images')
    permission_classes = [permissions.IsAuthenticated]
    

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        print(data)
        return data

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)