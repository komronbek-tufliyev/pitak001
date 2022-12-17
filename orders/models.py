from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from PIL import Image

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
    region = models.CharField(max_length=100, verbose_name=_('Viloyat'), choices=REGION_CHOICES, help_text=_("Viloyat nomi, 14ta tanlov bor."))
    district = models.CharField(max_length=50, verbose_name=_('Tuman'), help_text=_("Tuman nomi. M: Yunusobod"), blank=True, null=True)

    def __str__(self) -> str:
        return self.region + ', ' + self.district

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
    # phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message=_("Faqat O'zbekiston raqamlari kiriting"))
    # phone = models.CharField(_('phone number'), validators=[phone_regex], max_length=13, help_text=_('Phone number must be entered in the format: 9989XXXXXXXX'))
    # phone2 = models.CharField(_('phone number2'), validators=[phone_regex], max_length=13, unique=True, help_text=_('Phone number must be entered in the format: 9989XXXXXXXX'), null=True, blank=True)

    name = models.CharField(_('name'), max_length=50, blank=True, null=True, help_text=_("Buyurtma nomi(kiritlishi shart emas), ixtiyoriy."))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', help_text=_("Buyurtmachi id'si"))
    phone2 = models.CharField(_('phone number2'), max_length=13, help_text=_('Faqat o\'zbek raqamlari'), null=True, blank=True)
    car = models.CharField(_('car'), max_length=50, blank=True, null=True, help_text=_("Mashina nomi, M: Gentra"))
    car_number = models.CharField(_('car_number'), max_length=50, blank=True, null=True, help_text=_("Mashina raqami(shart emas), ixtiyoriy"))
    description = models.TextField(_('description'), blank=True, null=True, help_text=_("Buyurtma haqida qo'shimcha izoh"))
    # from_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='from_place')
    # to_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='to_place')
    from_place = models.CharField(max_length=100, verbose_name=_('From Place'), choices=REGION_CHOICES, help_text=_("Joy nomi, qayerdan..."))
    # to_place = models.CharField(max_length=100, verbose_name=_('To Place'), choices=REGION_CHOICES, help_text=_("Joy nomi, qayerga..."))
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='to_place', help_text=_("Joy nomi, qayerga..."))
    date = models.DateField(_('date'), blank=True, null=True, help_text=_("Buyurtma vaqti(ketish vaqti) YYYY-MM-DD HH:MM. M: 2022-12-25 09:00"))
    time = models.TimeField(_('time'), blank=True, null=True, help_text=_("Soat: HH:MM:SS, 09:00:00"))
    price = models.IntegerField(_('price'), blank=True, null=True, help_text=_("Narxi"))
    # left_back_free = models.BooleanField(_('orqa chap o\'rindiq'), default=True, help_text=_("Mashinaning chap orqa o'rindig'i bo'shmi?"))
    # right_back_free = models.BooleanField(_('orqa o\'ng o\'rindiq'), default=True, help_text=_("Mashinaning o'ng orqa o'rindig'i bo'shmi?"))
    # forward_free = models.BooleanField(_('haydovchi yonidagi o\'rindiq'), default=True, help_text=_("Haydovchi yonidagi o'rindig'i bo'shmi?"))
    # middle_free = models.BooleanField(_('orqa o\'rtadagi o\'rindiq'), default=True, help_text=_("Mashinaning o'rta o'rindig'i bo'shmi?"))
    # left_back_seat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leftbackseat') # default=None
    # right_back_seat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rightbackseat') # default=None
    # forward_seat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='forwardseat') # default=None
    # middle_seat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='middleseat') # default=None
    passengers = models.ManyToManyField('Seats', blank=True, help_text=_("Yo'lovchilar to'plami"), related_name='order_passengers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_driver = models.BooleanField(default=False, help_text=_("Buyurtmani beruvchi shaxs haydovchi bo'lsa True, aks holda False"))
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False, help_text=_("Status: qabul qilinganmi"))
    is_finished = models.BooleanField(default=False, help_text=_("Status: bajarilganmi"))
    is_canceled = models.BooleanField(default=False, help_text=_("Status: rad etilganmi"))
    is_paid = models.BooleanField(default=False, help_text=_("Status: to'langanmi"))
    # is_driver = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return self.owner.phone + ' ' + self.from_place + ' ' + str(self.to_place.pk)

    def get_order_short_info(self) -> str:
        return self.name

    def get_order_full_info(self) -> str:
        return self.name + ' Car: ' + self.car + ' owner: ' + self.owner.phone + 'from: ' + self.from_place + 'to: ' + str(self.to_place.pk)
    
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
        return self.to_place.pk

    def sort_by_owner(self):
        return self.owner.phone

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


# SEATS MODEL OF CAR
# class SeatsModel(models.Model):
#     left_back_seat = models.OneToOneField(User, verbose_name=_("orqadagi chap o'rindiq"), on_delete=models.SET_NULL, null=True, blank=True, related_name='leftbackseat_seatsmodel')
#     right_back_seat = models.OneToOneField(User, verbose_name=_("orqadagi o'ng o'rindiq"), on_delete=models.SET_NULL, null=True, blank=True, related_name='rightbackseat_seatsmodel') # default=None
#     forward_seat = models.OneToOneField(User, verbose_name=_("haydovchi yonidagi o'rindiq"), on_delete=models.SET_NULL, null=True, blank=True, related_name='forwardseat_seatsmodel') # default=None
#     middle_seat = models.OneToOneField(User, verbose_name=_("orqadagi o'rta o'rindiq"), on_delete=models.SET_NULL, null=True, blank=True, related_name='middleseat_seatsmodel') # default=None
#     order = models.OneToOneField(Order, verbose_name=_("Order "), on_delete=models.CASCADE, related_name='order_seatsmodel')

#     def __str__(self) -> str:
#         return f"order_id: {self.order.pk} + seats_id: {self.pk}"

class Seats(models.Model):
    SEAT_CHOICES = (
        # ('left_back', 'left_back'),
        # ('right_back', 'right_back'),
        # ('forward', 'forward'),
        # ('middle', 'middle')
        (1, 'forward'), 
        (2, 'right_back'),
        (3, 'middle'), 
        (4, 'left_back'),
    )
    user = models.ForeignKey(User, related_name='seat_model_user', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='seat_model_order', on_delete=models.CASCADE)
    seat = models.CharField(max_length=20, choices=SEAT_CHOICES)

    def __str__(self) -> str:
        return f"{self.seat}/ order: {self.order.pk}, user: {self.user.pk}"  


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


class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text=_("Buyurtma raqami(id)"), related_name="images")
    image = models.ImageField(upload_to='orders/%Y/%m/%d/', help_text=_("Buyurtirilgan mashina rasmi"))
    
    class Meta:
        verbose_name = _('Order Image')
        verbose_name_plural = _('Order Images')

    def __str__(self) -> str:
        return f"{self.pk} '+' {self.order.pk}. Media"

    def save(self, *args, **kwargs):
        super().save()

        try:
            img = Image.open(self.image.path)

            if img.height > 100 or img.width > 100:
                new_img = (100, 100)
                img.thumbnail(new_img)
                img.save(self.image.path)
        except:
            print("Error occured in order models.py", Exception)
            pass

