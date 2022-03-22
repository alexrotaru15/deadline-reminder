from distutils.command.clean import clean
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models import Q
from phonenumber_field.formfields import PhoneNumberField
from reminders.models import Phone


REQUIRED_ERROR = 'Acest câmp este obligatoriu.'

class RegisterForm(forms.Form):
    username = forms.CharField(label='Utilizator', error_messages={'required': REQUIRED_ERROR, 'min_length': 'Introduceți cel puțin 5 caractere.', 'max_length': 'Introduceți maxim 150 de caractere.'}, validators=[MinLengthValidator(5), MaxLengthValidator(150)])
    email = forms.EmailField(error_messages={'required': REQUIRED_ERROR, 'invalid': 'Adresa de email nu este validă'}, validators=[EmailValidator])
    phone = PhoneNumberField(widget=forms.TextInput(), required=False, error_messages={'required': REQUIRED_ERROR})
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Parola nu este la fel.')
        try:
            user = User.objects.get(Q(username=self.cleaned_data['username']) | Q(email=self.cleaned_data['email']))
        except ObjectDoesNotExist:
            user = None
        if user is not None:
            if user.username == cleaned_data.get('username'):
                self.add_error('username', 'Există deja un utilizator cu acest nume')
            if user.email == cleaned_data.get('email'):
                self.add_error('email', 'Există deja un utilizator cu această adresă de email')
        try:
            user_phone_number = Phone.objects.get(phone_number=cleaned_data.get('phone'))
        except ObjectDoesNotExist:
            user_phone_number = None
        if user_phone_number is not None:
            if user_phone_number.phone_number == cleaned_data.get('phone'):
                self.add_error('phone', 'Există deja un utilizator cu acest număr de telefon')


class ProfileForm(RegisterForm):
    password = None
    confirm_password = None
