from django.dispatch import receiver
from django.core.signals import request_finished
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete, m2m_changed

from .models import (
    Order,
    Seats,
    Place
)
from users.models import User
print("Running signals.py before imporing fcm_manager")

from .local_libs import FCMManager as fcm

print("Running signals.py")

@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:
        print("Order created ", instance)
        try:
            order_owner = instance.owner
            print("Order owner", order_owner)
        except Exception as e:
            print("error ", e)
            pass
        print("Order created", instance)
        print("order sender is ", sender)
    
@receiver(post_save, sender=Seats)
def create_seats(sender, instance, created, **kwargs):
    if created:
        try:
            title = f"Sizning mashinangizga yana bir odam buyurtma berdi"
            message = f"Buyurtma beruvchi tel: {instance.user.phone}"
            seat_owner = instance.order.owner
            registration_tokens = seat_owner.get_device_tokens()
            print("Seat owner", seat_owner)
            print("Device tokens", seat_owner.get_device_tokens())
            fcm.send_push(title=title, message=message, registraton_token=registration_tokens)
        except Exception as e:
            print("error ", e)
            pass
        print("Seats created instance: ", instance)
        print("Seats created sender: ", sender)

@receiver(post_delete, sender=Order)
def delete_order(sender, instance, *args, **kwargs):
    print("Order deleted instance: ", instance)
    print("Order deleted sender: ", sender)

@receiver(post_delete, sender=Seats)
def delete_seats(sender, instance, *args, **kwargs):

    # order_qs = sender.order
    # print("Order passengers", order_qs.passengers.all())
    # print("Order qs", order_qs)
    # print("Order ", sender)
    print("Deleted seats instance: ", instance)
    print("Deleted seats sender: ", sender)

# @receiver(m2m_changed, sender=Order.passengers.through)
# def seat_deleted(sender, **kwargs):
#     print("Kwargs of m2m changed, ", kwargs)
#     action = kwargs.pop('action', None)
#     pk_set = kwargs.pop('pk_set', None)
#     if action == "pre_delete":
#         print("Action pre_delete")
    