from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.core.validators import RegexValidator


# Create your models here.


class User(AbstractBaseUser):
    _USER_ERROR_MESSAGE = _("Bunday raqamli foydalanuvchi mavjud")

    phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message=_("Faqat O'zbekiston raqamlari kiriting"))
    phone = models.CharField(_('phone number'), validators=[phone_regex], max_length=13, unique=True, help_text=_('Phone number must be entered in the format: 9989XXXXXXXX'))
    phone2 = models.CharField(_('phone number2'), validators=[phone_regex], max_length=13, unique=True, help_text=_('Phone number must be entered in the format: 9989XXXXXXXX'), null=True, blank=True)

    name = models.CharField(_('name'), max_length=50, blank=True, null=True, help_text=_("To'liq ism. M: Falonchiyev Pistonchi"))
    is_driver = models.BooleanField(default=False, help_text=_("Haydovchimi"))
    device_token = models.CharField(max_length=255, null=True, blank=True, help_text=_("Qurilmaga berilgan token(shart emas)"))
    
    first_login = models.BooleanField(default=True, help_text=_("Birinchi marta login qilib kiryaptimi?"))

    favourite = models.ManyToManyField('orders.Order', related_name='favourite_order')

    is_active = models.BooleanField(default=True, help_text=_("Faolmi (hozir ham ishlatyaptimi)?"))
    is_staff = models.BooleanField(default=False, help_text=_("Xodimmi?"))
    is_superuser = models.BooleanField(default=False, help_text=_("Super adminmi?"))
    # is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone
    

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        if self.name:
            return self.name
        return self.phone

    def get_short_name(self):
        return self.phone

    # @property
    # def is_admin(self):
    #     return self.is_superuser

    # @property
    # def is_staff(self):
    #     return self.is_staff
    
    # @property
    # def is_active(self):
    #     return self.is_active
    

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_username(self):
        return self.phone

    def get_phone(self):
        return self.phone

class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message=_("Faqat O'zbekiston raqamlari kiriting"))
    phone = models.CharField(max_length=13, unique=True, validators=[phone_regex])
    otp = models.CharField(max_length=6, help_text=_("Bir martalik kodd. M: 1234"))
    count = models.IntegerField(default=0, help_text=_("Raqam tasdiqlanguncha yuborilgan SMSlar soni"))
    is_verified = models.BooleanField(default=False, help_text=_("Tasdiqlandimi?"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp + ' sent to ' + self.phone

    class Meta:
        verbose_name = _('Phone OTP')
        verbose_name_plural = _('Phone OTPS')

    def get_phone(self):
        return self.phone

    def get_otp(self):
        return self.otp

class SMSToken(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, help_text=_("SMS token nomi"))
    token = models.CharField(max_length=50, blank=True, null=True, help_text=_("Token nomi"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("..vaqtda yaratilgan"))
    expires_at = models.DateTimeField(blank=True, null=True, help_text=_("..vaqtgacha amal qiladi"))

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = _('SMS Token')
        verbose_name_plural = _('SMS Tokens')

    def get_token(self):
        return self.token

class SMSLog(models.Model):
    phone = models.CharField(max_length=13, help_text=_("Telefon raqam"))
    message = models.TextField(help_text=_("Telefonga yuborilgan OTP(bir martalik kodd) mavjud xabar"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone + ' ' + self.message

    class Meta:
        verbose_name = _('SMS log')
        verbose_name_plural = _('SMS logs')

    def get_phone(self):
        return self.phone

    def get_message(self):
        return self.message
