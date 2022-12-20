from orders.models import Order, OrderImage, Place
from orders.serializers import BookSeatSerializer, SeatSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from orders.models import Seats



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
                old_seat = Seats.objects.filter(order=order, seat=request.data.get('order'), user=user)
                if not old_seat.exists():
                    serializer = SeatSerializer(data=request.data, context={'request': request, 'order': order})
                    if serializer.is_valid(raise_exception=True):
                        try:
                            serializer.save()
                            return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)
                        except Exception as e:
                            return  Response({'status': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return  Response({'status': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status': False, 'detail': 'Bu joy allaqachon band qilingan'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': False, 'detail': 'Bunday order topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": False, 'detail': 'Nimadur xato ketdi'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order', None)
        seat = request.data.get('seat', None)
        if order_id is not None:
            order =  Order.objects.filter(pk=order_id)
            if order.exists():
                order = order.first()
                old_seat = Seats.objects.filter(order=order, user=user, seat=seat)
                if old_seat.exists():
                    old_seat = old_seat.first().pk
                    Seats.objects.filter(pk=old_seat).first().delete()
                    return Response({'status':True, 'detail': 'Tanlangan joy muvaffaqqiyatli bekor qilindi'})

                return Response({'status': True, 'detail': 'Bunday joy tanlanmagan'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': False, 'detail': 'Bunday order topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": False, 'detail': 'Nimadur xato ketdi'}, status=status.HTTP_400_BAD_REQUEST)

class GetSeatView(generics.ListAPIView):
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']
    
    def get_queryset(self):
        user = self.request.user
        if 'order_id' in self.kwargs:
            order_id = self.kwargs.get('order_id')
            order = Order.objects.filter(pk=order_id)
            if order.exists():
                order = order.first()
                seat = Seats.objects.filter(order=order)
                return seat
        return None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)