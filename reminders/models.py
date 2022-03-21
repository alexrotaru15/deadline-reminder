from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField

class Reminder(models.Model):
    CATEGORIES = [
        ('house', 'Casă'),
        ('car', 'Mașină'),
        ('work', 'Muncă'),
        ('others', 'Altele')
    ]
    category = models.CharField(max_length=6, null=False, blank=False, choices=CATEGORIES)
    title = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5)])
    description = models.TextField(max_length=500, null=False, blank=False)
    deadline_date = models.DateTimeField(null=False, blank=False)
    reminder_date = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return f"{self.phone_number}"


class Contact(models.Model):
    by_phone = models.BooleanField("Contact via phone")
    by_email = models.BooleanField("Contact via email")
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"
