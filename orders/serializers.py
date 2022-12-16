from rest_framework import serializers
from .models import Order, OrderComment, Place, OrderImage
from users.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, ProfileSerializer
from django.conf import settings
User = get_user_model()


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        return Place.objects.create(**validated_data)

class FilterByPlaceSerializer(serializers.Serializer):
    region = serializers.CharField(required=True)

class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ['image', 'order']
        extra_kwargs = {'order': {'read_only': True}}


class OrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComment
        fields = '__all__'

    def create(self, validated_data):
        return OrderComment.objects.create(**validated_data)

class CreateOrderDisplaySerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True,)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True,
        required=False,
    )

    to_place = serializers.CharField()
    to_place_district = serializers.CharField()
    left_back_seat = ProfileSerializer()
    right_back_seat = ProfileSerializer()
    forward_seat = ProfileSerializer()
    middle_seat = ProfileSerializer()
    # date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    class Meta:
        model = Order 
        ref_name = 'Order display'
        fields = ['id', 'name', 'car', 'phone2','from_place', 'to_place', 'to_place_district', 'price', 'date', 'time', 'description', 'left_back_seat', 'right_back_seat', 'middle_seat', 'forward_seat', 'is_driver', 'is_active', 'is_paid', 'is_finished', 'is_accepted', 'is_canceled', 'images', 'uploaded_images']
        extra_kwargs = {"owner": {"read_only": True}}

class CreateOrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True,)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True,
        required=False,
    )

    # date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    # to_place = serializers.CharField()
    # to_place_district = serializers.CharField()

    class Meta:
        model = Order 
        ref_name = 'Order'
        fields = ['id', 'name', 'car', 'phone2','from_place', 'to_place', 'price', 'date', 'time', 'description', 'left_back_seat', 'right_back_seat', 'middle_seat', 'forward_seat', 'is_driver', 'is_active', 'is_paid', 'is_finished', 'is_accepted', 'is_canceled', 'images', 'uploaded_images']
        extra_kwargs = {"owner": {"read_only": True}}

    def create(self, validated_data):
        print("Validated data", validated_data)
        owner = self.context.get('owner')
        uploaded_images = validated_data.pop('uploaded_images', None)
        # to_place = validated_data.pop('to_place', None)
        # to_place_district = validated_data.pop('to_place_district', None)
        # if to_place and to_place_district:
        #     try:
        #         to_place = Place.objects.get(region=to_place, district=to_place_district)
        #     except Place.DoesNotExist:
        #         to_place = Place.objects.create(region=to_place, district=to_place_district)
        new_order = Order.objects.create(
            owner=owner,
            # to_place=to_place,
            **validated_data
        )
        print("New order", new_order)
        print("Ser images", uploaded_images)
        if uploaded_images:
            for image in uploaded_images:
                print("Order image", image)
                new_order_image = OrderImage.objects.create(order=new_order, image=image)

        return new_order

    def to_representation(self, instance):
        return super().to_representation(instance)

class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)
    to_place = PlaceSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    left_back_seat = ProfileSerializer()
    right_back_seat = ProfileSerializer()
    forward_seat = ProfileSerializer()
    middle_seat = ProfileSerializer()
    is_liked = serializers.BooleanField(read_only=True, help_text=_("Agar orderga like bosilgan bo'lsa is_liked=True bo'ladi"))
    # date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    class Meta:
        model = Order
        ref_name = 'Order Serializer'
        fields = ['id', 'name', 'owner', 'phone2', 'car', 'from_place', 'to_place', 'price', 'date', 'time', 'description', 'left_back_seat', 'right_back_seat', 'middle_seat', 'forward_seat', 'is_driver', 'is_active', 'is_accepted', 'is_finished', 'is_paid', 'images', 'is_liked']

    def to_representation(self, instance):
        # from pprint import pprint
        data = super().to_representation(instance)
        # print(data)
        user = self.context['request'].user
        # print("User", user)
        if user is not None:
            fav_order_ids = [order.pk for order in user.favourite.all()]
            # print("Fav order ids", fav_order_ids)
            if data.get('id') in fav_order_ids:
                # print("True")
                data.update({'is_liked': True})
            else:
                # print("False")
                data.update({'is_liked': False})
        return data


class OrderUpdateSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True,)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True,
        required=False,
    )
    # date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    # to_place = serializers.CharField()
    # to_place_district = serializers.CharField()

    def clear_existing_images(self, instance):
        for order_image in instance.orderimage_set.all():
            order_image.images.delete()
            order_image.delete()

    class Meta:
        model = Order 
        ref_name = 'Order'
        fields = ['id', 'name', 'car', 'phone2','from_place', 'to_place', 'price', 'date', 'time', 'description', 'left_back_seat', 'right_back_seat', 'middle_seat', 'forward_seat', 'is_driver', 'is_active', 'is_paid', 'is_finished', 'is_accepted', 'is_canceled', 'images', 'uploaded_images']
        extra_kwargs = {"owner": {"read_only": True}}

    def update(self, instance, validated_data):
        # print("Validated data", validated_data)
        owner = self.context.get('owner')
        uploaded_images = validated_data.pop('uploaded_images', None)
        instance.from_place = validated_data.get('from_place', instance.from_place)
        instance.to_place = validated_data.get('to_place', instance.to_place)
        instance.car = validated_data.get('car', instance.car)
        instance.car_number = validated_data.get('car_number', instance.car_number)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.left_back_seat = validated_data.get('left_back_seat', instance.left_back_seat) 
        instance.right_back_seat = validated_data.get('right_back_seat', instance.right_back_seat)
        instance.forward_seat = validated_data.get('forward_seat', instance.forward_seat)
        instance.middle_seat = validated_data.get('middle_seat', instance.middle_seat) 
        instance.is_driver = validated_data.get('is_driver', instance.is_driver)
        instance.is_finished = validated_data.get('is_finished', instance.is_finished)
        instance.is_canceled = validated_data.get('is_canceled', instance.is_canceled)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        # instance
        print("New order", instance)
        print("Ser images", uploaded_images)
        if uploaded_images:
            order_image_model_instance = [OrderImage(order=instance, image=image) for image in uploaded_images]
            OrderImage.objects.bulk_create(order_image_model_instance)
            # for image in uploaded_images:
            #     print("Order image", image)
            #     new_order_image = OrderImage.objects.create(order=instance, image=image)
        instance.save()
        return instance



class FavouriteOrderSerializer(serializers.ModelSerializer):
    favourite = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'favourite']

    def create(self, validated_data):
        user = self.context.get('user')
        order = self.context.get('order')
        if order:
            if order not in user.favourite.all():
                user.favourite.add(order)
                return user
        return user
    
    def to_representation(self, instance):
        return super().to_representation(instance)

class DisplayFavOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    