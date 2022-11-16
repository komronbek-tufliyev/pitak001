from rest_framework import serializers
from .models import Order, OrderComment, Place, OrderImage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


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

class CreateOrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True
    )

    class Meta:
        model = Order 
        fields = ['id', 'name', 'car', 'description', 'from_place', 'to_place', 'price', 'date', 'images', 'is_paid', 'is_finished', 'is_accepted', 'is_canceled', 'is_active', 'images', 'uploaded_images']
        extra_kwargs = {"owner": {"read_only": True}}

    def create(self, validated_data):
        print("Validated data", validated_data)
        owner = self.context.get('owner')
        uploaded_images = validated_data.pop('uploaded_images', None)
        new_order = Order.objects.create(
            owner=owner,
            **validated_data
        )
        print("New order", new_order)
        print("Ser images", uploaded_images)
        for image in uploaded_images:
            print("Order image", image)
            new_order_image = OrderImage.objects.create(order=new_order, image=image)
        return new_order

    def to_representation(self, instance):
        return super().to_representation(instance)

class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'name', 'owner', 'car', 'description', 'from_place', 'to_place', 'price', 'date', 'is_active', 'is_accepted', 'is_finished', 'is_paid', 'images']



class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        return Place.objects.create(**validated_data)