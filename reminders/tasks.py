from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Reminder


logger = get_task_logger(__name__)

# @shared_task(bind=True)
# def change_title_reminder(reminder_id, title):
#     r = Reminder(categories='car')
