from django.contrib import admin
from .models import (
    Order,
    OrderComment,
    OrderImage,
    Place,
    Likes,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


# Register your models here.


admin.site.register(Order)
admin.site.register(OrderComment)
admin.site.register(OrderImage)
admin.site.register(Place)
admin.site.unregister(Group)
admin.site.register(Likes)

