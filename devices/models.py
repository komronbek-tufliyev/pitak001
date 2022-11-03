from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


# Connected devices model
class Device(models.Model):
    DEVICE_TYPE_CHOICES = (
        ('android', 'Android'),
        ('ios', 'IOS'),
    )
    DEVICE_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=50, verbose_name=_('Device Name'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    device_type = models.CharField(max_length=50, verbose_name=_('Device Type'), choices=DEVICE_TYPE_CHOICES)
    device_status = models.CharField(max_length=50, verbose_name=_('Device Status'), choices=DEVICE_STATUS_CHOICES)
    app_version = models.CharField(max_length=50, verbose_name=_('App Version'))
    # device_id = models.CharField(max_length=50, verbose_name=_('Device ID'))


    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

# Connected devices model
class DeviceToken(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Device Token Name'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=50, verbose_name=_('Device Token'))
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_tokens')


    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Device Token')
        verbose_name_plural = _('Device Tokens')


