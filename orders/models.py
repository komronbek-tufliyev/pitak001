from django.db import models
from django.utils.translation import gettext_lazy as _ 
# from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.signals import request_finished, request_started

from django.dispatch import receiver
from django.conf import settings

from users.models import User

User = get_user_model()
# Create your models here.


class Place(models.Model):
    # uzbek regions
    REGION_CHOICES = (
        ('Toshkent', 'Toshkent'),
        ('Andijon', 'Andijon'),
        ('Buxoro', 'Buxoro'),
        ('Farg\'ona', 'Farg\'ona'),
        ('Jizzax', 'Jizzax'),
        ('Namangan', 'Namangan'),
        ('Navoiy', 'Navoiy'),
        ('Qashqadaryo', 'Qashqadaryo'),
        ('Qoraqalpog\'iston Respublikasi', 'Qoraqalpog\'iston Respublikasi'),
        ('Samarqand', 'Samarqand'),
        ('Sirdaryo', 'Sirdaryo'),
        ('Surxondaryo', 'Surxondaryo'),
        ('Toshkent vil', 'Toshkent vil'),
        ('Xorazm', 'Xorazm'),

    )
    name = models.CharField(max_length=50, verbose_name=_('Place Name'))
    region = models.CharField(max_length=100, verbose_name=_('Region'), choices=REGION_CHOICES)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')


# Taxi order model
class Order(models.Model):
     # uzbek regions
    REGION_CHOICES = (
        ('Toshkent', 'Toshkent'),
        ('Andijon', 'Andijon'),
        ('Buxoro', 'Buxoro'),
        ('Farg\'ona', 'Farg\'ona'),
        ('Jizzax', 'Jizzax'),
        ('Namangan', 'Namangan'),
        ('Navoiy', 'Navoiy'),
        ('Qashqadaryo', 'Qashqadaryo'),
        ('Qoraqalpog\'iston Respublikasi', 'Qoraqalpog\'iston Respublikasi'),
        ('Samarqand', 'Samarqand'),
        ('Sirdaryo', 'Sirdaryo'),
        ('Surxondaryo', 'Surxondaryo'),
        ('Toshkent vil', 'Toshkent vil'),
        ('Xorazm', 'Xorazm'),

    )
    _ORDER_ERROR_MESSAGE = _("Order error message")
    name = models.CharField(_('name'), max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.CharField(_('car'), max_length=50, blank=True, null=True)
    car_number = models.CharField(_('car_number'), max_length=50, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    # from_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='from_place')
    # to_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='to_place')
    from_place = models.CharField(max_length=100, verbose_name=_('From Place'), choices=REGION_CHOICES)
    to_place = models.CharField(max_length=100, verbose_name=_('To Place'), choices=REGION_CHOICES)
    date = models.DateField(_('date'), blank=True, null=True)
    price = models.IntegerField(_('price'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='images/orders/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return self.owner.phone + ' ' + self.from_place.name + ' ' + self.to_place.name

    def get_order_short_info(self) -> str:
        return self.name

    def get_order_full_info(self) -> str:
        return self.name + ' Car: ' + self.car + ' owner: ' + self.owner.phone + 'from: ' + self.from_place.name + 'to: ' + self.to_place.name
    
    def get_order_owner(self) -> str:
        return self.owner

    def get_order_car(self) -> str:
        return self.car
    
    def get_status(self) -> str:
        if self.is_accepted:
            return 'Accepted'
        elif self.is_finished:
            return 'Finished'
        elif self.is_canceled:
            return 'Canceled'
        elif self.is_paid:
            return 'Paid'
        elif self.is_driver:
            return 'Driver'
        else:
            return 'New'
    
    def get_price(self) -> str:
        return self.price

    def sort_by_date(self):
        return self.date

    def sort_by_from_place(self):
        return self.from_place

    def sort_by_to_place(self):
        return self.to_place

    def sort_by_owner(self):
        return self.owner.phone


    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

class OrderComment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(_('comment'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.comment

    class Meta:
        verbose_name = _('Order Comment')
        verbose_name_plural = _('Order Comments')


class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='order_files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.file

    class Meta:
        verbose_name = _('Order File')
        verbose_name_plural = _('Order Files')

