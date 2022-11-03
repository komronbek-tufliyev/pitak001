from django.contrib import admin
from .models import (
    Order,
    OrderComment,
    OrderFile,
    Place,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


# Register your models here.


admin.site.register(Order)
admin.site.register(OrderComment)
admin.site.register(OrderFile)
admin.site.register(Place)
admin.site.unregister(Group)


