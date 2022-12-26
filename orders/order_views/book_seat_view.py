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
                old_seat = Seats.objects.filter(order=order, seat=request.data.get('seat'), user=user)
                if not old_seat.exists():
                    print("Bunday order mavjud emas va davom etyapman")
                    serializer = SeatSerializer(data=request.data, context={'request': request, 'order': order})
                    if serializer.is_valid(raise_exception=True):
                        try:
                            serializer.save()
                            print("Everything is working correctly")
                            return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)
                        except Exception as e:
                            print("Exception is working on /orders/seats/create/ route")
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
        if seat is None or order_id is None:
            return Response({'status': False, 'detail': 'order va seat berilishi shart'}, status=status.HTTP_400_BAD_REQUEST)
        if order_id is not None:
            order =  Order.objects.filter(pk=order_id)
            if order.exists():
                order = order.first()
                old_seat = Seats.objects.filter(order=order, seat=seat)
                if old_seat.exists():
                    if old_seat.first().user != user:
                        return Response({'status': False, 'detail': 'Bu joyni o\'chirishga vakolatingiz yo\'q'}, status=status.HTTP_403_FORBIDDEN)
                    old_seat = old_seat.first().pk
                    Seats.objects.filter(pk=old_seat).first().delete()
                    return Response({'status':True, 'detail': 'Tanlangan joy muvaffaqqiyatli bekor qilindi'}, status=status.HTTP_200_OK)

                return Response({'status': True, 'detail': 'Bunday joy tanlanmagan'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': False, 'detail': 'Bunday order topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": False, 'detail': 'Nimadur xato ketdi'}, status=status.HTTP_400_BAD_REQUEST)

class GetSeatView(APIView):
    # serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']
    
    def get(self, request, format=None):
        order_id = request.data.get('order', None)
        if order_id is not None:
            order = Order.objects.filter(pk=order_id)
            if order.exists():
                order = order.first()
                seat = Seats.objects.filter(order=order).all()
                if seat is not None:
                    serializer = SeatSerializer(seat, many=True)
                    return Response({'status': True, 'detail': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'detail': []}, status=status.HTTP_200_OK)
            return Response({'status': False, 'detail': 'Bunday id-ga ega order topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': False, 'detail': 'order must required'}, status=status.HTTP_400_BAD_REQUEST)
            

