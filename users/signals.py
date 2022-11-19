from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.signals import request_finished, request_started, got_request_exception
from .models import (
    User,
    SMSLog,
    PhoneOTP,
    SMSToken,
)

User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        print('user_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('user_post_save')

@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    print('user_pre_save')
    print(instance)
    print(kwargs)
    print('user_pre_save')

@receiver(post_save, sender=SMSLog)
def sms_log_post_save(sender, instance, created, **kwargs):

    if created:
        print('sms_log_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('sms_log_post_save')

@receiver(pre_save, sender=SMSLog)
def sms_log_pre_save(sender, instance, **kwargs):
    print('sms_log_pre_save')
    print(instance)
    print(kwargs)
    print('sms_log_pre_save')

@receiver(post_save, sender=PhoneOTP)
def phone_otp_post_save(sender, instance, created, **kwargs):
    if created:
        print('phone_otp_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('phone_otp_post_save')

@receiver(pre_save, sender=PhoneOTP)
def phone_otp_pre_save(sender, instance, **kwargs):
    print('phone_otp_pre_save')
    print(instance)
    print(kwargs)
    print('phone_otp_pre_save')

@receiver(post_save, sender=SMSToken)
def sms_token_post_save(sender, instance, created, **kwargs):
    if created:
        print('sms_token_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('sms_token_post_save')

@receiver(pre_save, sender=SMSToken)
def sms_token_pre_save(sender, instance, **kwargs):
    print('sms_token_pre_save')
    print(instance)
    print(kwargs)
    print('sms_token_pre_save')

@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    print('user_pre_delete')
    print(instance)
    print(kwargs)
    print('user_pre_delete')

@receiver(post_delete, sender=User)
def user_post_delete(sender, instance, **kwargs):
    print('user_post_delete')
    print(instance)
    print(kwargs)
    print('user_post_delete')

@receiver(pre_delete, sender=SMSLog)
def sms_log_pre_delete(sender, instance, **kwargs):
    print('sms_log_pre_delete')
    print(instance)
    print(kwargs)
    print('sms_log_pre_delete')

@receiver(post_delete, sender=SMSLog)
def sms_log_post_delete(sender, instance, **kwargs):
    print('sms_log_post_delete')
    print(instance)
    print(kwargs)
    print('sms_log_post_delete')

@receiver(pre_delete, sender=PhoneOTP)
def phone_otp_pre_delete(sender, instance, **kwargs):
    print('phone_otp_pre_delete')
    print(instance)
    print(kwargs)
    print('phone_otp_pre_delete')

@receiver(post_delete, sender=PhoneOTP)
def phone_otp_post_delete(sender, instance, **kwargs):
    print('phone_otp_post_delete')
    print(instance)
    print(kwargs)
    print('phone_otp_post_delete')

@receiver(pre_delete, sender=SMSToken)
def sms_token_pre_delete(sender, instance, **kwargs):
    print('sms_token_pre_delete')
    print(instance)
    print(kwargs)
    print('sms_token_pre_delete')

@receiver(post_delete, sender=SMSToken)
def sms_token_post_delete(sender, instance, **kwargs):
    print('sms_token_post_delete')
    print(instance)
    print(kwargs)
    print('sms_token_post_delete')


request_finished.connect(user_post_save)
request_finished.connect(user_pre_save)
request_finished.connect(sms_log_post_save)
request_finished.connect(sms_log_pre_save)
request_finished.connect(phone_otp_post_save)
request_finished.connect(phone_otp_pre_save)
request_finished.connect(sms_token_post_save)
request_finished.connect(sms_token_pre_save)
request_finished.connect(user_pre_delete)
request_finished.connect(user_post_delete)
request_finished.connect(sms_log_pre_delete)
request_finished.connect(sms_log_post_delete)
request_finished.connect(sms_token_post_delete)
request_finished.connect(sms_token_pre_delete)
request_finished.connect(phone_otp_pre_delete)
request_finished.connect(phone_otp_post_delete)

    

