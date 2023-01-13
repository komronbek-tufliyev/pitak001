from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .models import User, Device


@receiver(user_logged_in)
def logged_in_user(sender, user, request, **kwargs):
    print("User logged in instance: ", user)
    print("Request", request)
    

user_logged_in.connect(logged_in_user)

@receiver(user_logged_out)
def logged_out_user(sender, user, request, **kwargs):
    print("User logged out instance: ", user)
    print("Request", request)

user_logged_out.connect(logged_out_user)


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        print("User created instance: ", instance)

@receiver(post_delete, sender=User)
def delete_user(sender, instance, *args, **kwargs):
    print("User deleted instance: ", instance)

@receiver(post_save, sender=Device)
def create_device(sender, instance, created, **kwargs):
    if created:
        print("Device created instance: ", instance)
        print("Device token: ", instance.get_device_token())
       

@receiver(post_delete, sender=Device)
def delete_device(sender, instance, *args, **kwargs):
    print("Device deleted instance: ", instance)