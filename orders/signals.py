from .models import (
    Order,  
    OrderComment,
    OrderFile,
    Place,
)
from django.core.signals import request_finished, request_started
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        print('order_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('order_post_save')

@receiver(post_save, sender=OrderComment)
def order_comment_post_save(sender, instance, created, **kwargs):
    if created:
        print('order_comment_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('order_comment_post_save')

@receiver(post_save, sender=OrderFile)
def order_file_post_save(sender, instance, created, **kwargs):
    if created:
        print('order_file_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('order_file_post_save')

@receiver(post_save, sender=Place)
def place_post_save(sender, instance, created, **kwargs):
    if created:
        print('place_post_save')
        print(instance)
        print(created)
        print(kwargs)
        print('place_post_save')

@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    print('order_pre_save')
    print(instance)
    print(kwargs)
    print('order_pre_save')

@receiver(pre_save, sender=OrderComment)
def order_comment_pre_save(sender, instance, **kwargs):
    print('order_comment_pre_save')
    print(instance)
    print(kwargs)
    print('order_comment_pre_save')

@receiver(pre_save, sender=OrderFile)
def order_file_pre_save(sender, instance, **kwargs):
    print('order_file_pre_save')
    print(instance)
    print(kwargs)
    print('order_file_pre_save')

@receiver(pre_save, sender=Place)
def place_pre_save(sender, instance, **kwargs):
    print('place_pre_save')
    print(instance)
    print(kwargs)
    print('place_pre_save')

@receiver(pre_delete, sender=Order)
def order_pre_delete(sender, instance, **kwargs):
    print('order_pre_delete')
    print(instance)
    print(kwargs)
    print('order_pre_delete')

@receiver(pre_delete, sender=OrderComment)
def order_comment_pre_delete(sender, instance, **kwargs):
    print('order_comment_pre_delete')
    print(instance)
    print(kwargs)
    print('order_comment_pre_delete')

@receiver(pre_delete, sender=OrderFile)
def order_file_pre_delete(sender, instance, **kwargs):

    print('order_file_pre_delete')
    print(instance)
    print(kwargs)
    print('order_file_pre_delete')

@receiver(pre_delete, sender=Place)
def place_pre_delete(sender, instance, **kwargs):
    print('place_pre_delete')
    print(instance)
    print(kwargs)
    print('place_pre_delete')

@receiver(post_delete, sender=Order)
def order_post_delete(sender, instance, **kwargs):
    print('order_post_delete')
    print(instance)
    print(kwargs)
    print('order_post_delete')

@receiver(post_delete, sender=OrderComment)
def order_comment_post_delete(sender, instance, **kwargs):
    print('order_comment_post_delete')
    print(instance)
    print(kwargs)
    print('order_comment_post_delete')

@receiver(post_delete, sender=OrderFile)
def order_file_post_delete(sender, instance, **kwargs):
    print('order_file_post_delete')
    print(instance)
    print(kwargs)
    print('order_file_post_delete')

@receiver(post_delete, sender=Place)
def place_post_delete(sender, instance, **kwargs):
    print('place_post_delete')
    print(instance)
    print(kwargs)
    print('place_post_delete')


request_finished.connect(order_post_save)
# request_started.connect(order_comment_post_save)
request_finished.connect(order_file_post_save)
# request_started.connect(place_post_save)
request_finished.connect(order_pre_save)
# request_started.connect(order_comment_pre_save)
request_finished.connect(order_file_pre_save)
# request_started.connect(place_pre_save)
request_finished.connect(order_pre_delete)
# request_started.connect(order_comment_pre_delete)
request_finished.connect(order_file_pre_delete)
# request_started.connect(place_pre_delete)
request_finished.connect(order_post_delete)

# request_started.connect(order_comment_post_delete)
request_finished.connect(order_file_post_delete)
# request_started.connect(place_post_delete)
