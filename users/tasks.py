from celery import shared_task
from users.models import Notification, User
from django.utils import timezone
from datetime import timedelta


@shared_task(name='change_ban_status')
def change_ban_status():
    day_threshold = timezone.now()-timedelta(days=30)
    User.objects.exclude(date_banned__isnull=True).filter(
        date_banned__lte=day_threshold).update(date_banned=None)
