from tkinter.messagebox import NO
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField

class Reminder(models.Model):
    categories = [
        ('house', 'Casă'),
        ('car', 'Mașină'),
        ('work', 'Muncă'),
        ('others', 'Altele')
    ]
    timers = [
        (30, '30 de minute'),
        (60, '1 oră'),
        (60 * 3, '3 ore'),
        (60 * 12, '12 ore'),
        (60 * 24, 'o zi'),
        (60 * 48, '2 zile'),
        (60 * 24 * 7, '7 zile')
    ]
    category = models.CharField(
        max_length=6, 
        null=False, 
        blank=False, 
        choices=categories
    )
    title = models.CharField(
        max_length=50, 
        null=False, 
        blank=False, 
        validators=[MinLengthValidator(3)]
    )
    description = models.TextField(
        max_length=500, 
        null=True, 
        blank=True
    )
    deadline_date = models.DateTimeField(
        null=False, 
        blank=False
    )
    reminder_time = models.CharField(
        'Cu cât timp înainte doriți să primiți notificare?',
        max_length=10,
        choices=timers
        )
    reminder_date = models.DateTimeField(
        null=False, 
        blank=False
    )
    by_phone = models.BooleanField("Contact via phone")
    by_email = models.BooleanField("Contact via email")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        super(Reminder, self).clean()
        if self.deadline_date is not None and self.deadline_date < timezone.now():
            raise ValidationError({'deadline_date': 'Nu puteți selecta o dată din trecut.'})
        if not self.by_phone and not self.by_email:
            raise ValidationError({'by_phone': 'Trebuie să selectați cel puțin o opțiune de contact', 'by_email': ''})
        
    def __str__(self):
        return f"{self.user.username}"


class Phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        null=False, 
        blank=False, 
        unique=True
    )

    def __str__(self):
        return f"{self.phone_number}"
