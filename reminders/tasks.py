from __future__ import absolute_import, unicode_literals
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Reminder


logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    logger.info('task started')
    return x + y

# @shared_task(bind=True)
# def new_reminder(self, user_id):
#     r = Reminder(
#         category='car',
#         title=f'title-{timezone.now()}',
#         description=f'description for reminder with title=title-{timezone.now()}',
#         deadline_date=timezone.now() + datetime.timedelta(days=1, minutes=60),
#         reminder_time=30,
#         reminder_date=timezone.now() + datetime.timedelta(days=1, minutes=30),
#         by_phone=True,
#         by_email=False,
#         user=User.objects.get(pk=user_id)
#         )
#     r.save()
