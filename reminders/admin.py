from django.contrib import admin
from .models import Reminder, Contact, Phone

admin.site.register(Reminder)
admin.site.register(Contact)
admin.site.register(Phone)
