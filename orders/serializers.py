from rest_framework import serializers
from .models import Order, OrderComment, OrderFile, Place
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers    

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComment
        fields = '__all__'

    def create(self, validated_data):
        return OrderComment.objects.create(**validated_data)

class CreateOrderSerializer(serializers.Serializer):
    images =  serializers.ListField(
        child=Base64ImageField(
            max_length=None, use_url=True,
        )
    )

    class Meta:
        model = Order 
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        print("V_data: ", validated_data)
        # validated_data = validated_data.pop('validated_data')
        print("V data: ", validated_data)
        # owner_id = validated_data.pop('owner')
        images = validated_data.pop('images')
        owner = validated_data.pop('owner')
        print("Owner: ", owner)
        print("Images: ", images)

        # owner = validated_data.pop('owner')
        print("Args", args)
        print("Kwargs", kwargs)
        # print("Owner", owner_id)
        # from_place = int(validated_data.pop('from_place')[0])
        # to_place = int(validated_data.pop('to_place')[0])
        image_lists = []
        print("VALIDATED DATA", validated_data)
        print("IMAGES", len(images))
        for image in images:
            photo = Order.objects.create(image=image, **validated_data)
            image_lists.append(photo.image.url)
        return image_lists

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        return Place.objects.create(**validated_data)