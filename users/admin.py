from django.contrib import admin
from .models import (
    User,
    PhoneOTP, 
    SMSLog, 
    SMSToken,
)
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(SMSLog)
admin.site.register(SMSToken)
# admin.site.unregister(Group)



class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'is_driver', 'is_active', 'is_superuser']
    list_filter = ['is_superuser', 'is_active', 'is_staff', 'is_driver']
    search_fields = ['phone', 'name']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'is_driver', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_driver')}
        ),
    )
    filter_horizontal = []

    
admin.site.register(User, UserAdmin)


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'otp', 'count', 'created_at', 'is_verified']
    list_filter = ['is_verified', 'count']
    search_fields = ['phone', 'otp']

    filter_horizontal = []

admin.site.register(PhoneOTP, PhoneOTPAdmin)




