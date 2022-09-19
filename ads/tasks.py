from celery import shared_task
from users.models import Notification


@shared_task
def send_ad_creation(ad):
    Notification.objects.create(
        user=ad.user, text='Your advertisement was successfully created.please wait until your ad is verified.')


@shared_task
def send_ad_verification(ad):
    Notification.objects.create(
        user=ad.user, text='Your advertisement was successfully verified.')


@shared_task
def send_message_notification(message):
    Notification.objects.create(
        user=message.user, text='you receved a message for yor published ad.')
