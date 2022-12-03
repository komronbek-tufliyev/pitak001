from django.contrib import admin
from .models import (
    Order,
    OrderComment,
    OrderImage,
    Place,
    # Likes,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


# Register your models here.
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'district',)
    search_fields = ('region', 'district', )
    list_filter = ('region', )
    list_per_page = 25

admin.site.register(Place, PlaceAdmin)


# admin.site.register(OrderComment)
class OrderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'image')
    search_fields = ('order', 'image', )
    list_filter = ('order', 'image', )
    list_per_page = 25

class ImageAdmin(admin.StackedInline):
    model = OrderImage

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'from_place', 'to_place', 'description', 'date', 'price')
    search_fields = ('owner', 'name', 'from_place', 'description', 'price', )
    list_filter = ('owner', 'from_place', 'to_place', 'date', )
    list_per_page = 25
    inlines = [ImageAdmin, ]

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderImage, OrderImageAdmin)
admin.site.unregister(Group)
# admin.site.register(Likes)

