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

admin.site.register(Order)
# admin.site.register(OrderComment)
class OrderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'image')
    search_fields = ('order', 'image', )
    list_filter = ('order', 'image', )
    list_per_page = 25


admin.site.register(OrderImage, OrderImageAdmin)
admin.site.unregister(Group)
# admin.site.register(Likes)

