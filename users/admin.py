from django.contrib import admin
from .models import (
    User,
    PhoneOTP, 
    SMSLog, 
    SMSToken,
)
from django.contrib.auth.models import Group
from rest_framework_simplejwt import tokens, token_blacklist

# Register your models here.

admin.site.register(SMSLog)
admin.site.register(SMSToken)
# admin.site.unregister(Group)



class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'is_driver', 'is_active', 'is_superuser', 'get_favourites']
    list_filter = ['is_superuser', 'is_active', 'is_staff', 'is_driver']
    search_fields = ['phone', 'name']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'is_driver', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        # ('Favourite Orders', {'fields': ('get_favourites',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_driver', )}
        ),
    )
    filter_horizontal = []

    def get_favourites(self, obj):
        if obj.favourite.all():
            return f"Order_ids: {list(obj.favourite.all().values_list('pk', flat=True))}"
        else:
            return 'No favourite orders'
        # return self.favourite.pk

    
admin.site.register(User, UserAdmin)


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'otp', 'count', 'created_at', 'is_verified']
    list_filter = ['is_verified', 'count']
    search_fields = ['phone', 'otp']

    filter_horizontal = []

admin.site.register(PhoneOTP, PhoneOTPAdmin)

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

