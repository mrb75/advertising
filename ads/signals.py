from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import Ad, Message
from . import tasks


@receiver(post_save, sender=Ad)
def send_add_ad_notification(sender, **kwargs):
    if kwargs['created']:
        tasks.send_ad_creation(kwargs['instance'])
    else:
        if kwargs['update_fields'] and ('is_verified' in kwargs['update_fields']) and kwargs['instance'].is_verified:
            tasks.send_ad_verification(kwargs['instance'])


@receiver(post_save, sender=Message)
def send_message_notification(sender, **kwargs):
    if kwargs['created']:
        tasks.send_message_notification(kwargs['instance'])
