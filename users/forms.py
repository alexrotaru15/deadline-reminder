from distutils.command.clean import clean
from django import forms
from django.core.validators import MaxLengthValidator, EmailValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils.translation import ngettext
from django.db.models import Q
from phonenumber_field.formfields import PhoneNumberField
from reminders.models import Phone


REQUIRED_ERROR = 'Acest câmp este obligatoriu.'

class RegisterForm(forms.Form):
    username = forms.CharField(label='Utilizator', error_messages={'required': REQUIRED_ERROR, 'max_length': 'Introduceți maxim 150 de caractere.'}, validators=[MaxLengthValidator(50)])
    email = forms.EmailField(error_messages={'required': REQUIRED_ERROR, 'invalid': 'Adresa de email nu este validă'}, validators=[EmailValidator])
    phone = PhoneNumberField(label="Telefon", widget=forms.TextInput(), required=False, error_messages={'required': REQUIRED_ERROR, 'invalid': 'Numărul de telefon nu este valid.'})
    password = forms.CharField(label="Parolă" ,widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirmare Parolă",widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data['username']
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Câmpurile 'Parolă' și 'Confirmare Parolă' trebuie să coincidă.")
        try:
            user = User.objects.get(Q(username=username) | Q(email=cleaned_data['email']))
        except ObjectDoesNotExist:
            user = None
        if user is not None:
            if user.username == username:
                self.add_error('username', 'Există deja un utilizator cu acest nume.')
            if user.email == cleaned_data.get('email'):
                self.add_error('email', 'Există deja un utilizator cu această adresă de email.')
        try:
            user_phone_number = Phone.objects.get(phone_number=cleaned_data.get('phone'))
        except ObjectDoesNotExist:
            user_phone_number = None
        if user_phone_number is not None:
            if user_phone_number.phone_number == cleaned_data.get('phone'):
                self.add_error('phone', 'Există deja un utilizator cu acest număr de telefon.')


class ProfileForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.user.username
        self.fields['email'].initial = self.user.email
        self.fields['phone'].initial = self.user.phone.phone_number
    password = None
    confirm_password = None

    def clean(self):
        pass


class CMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=5):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Parola este prea scurtă. Aceasta trebuie să conțină cel puțin "
                    "%(min_length)d caracter.",
                    "Parola este prea scurtă. Aceasta trebuie să conțină cel puțin "
                    "%(min_length)d caractere.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Parola trebuie să conțină cel puțin %(min_length)d characte.",
            "Parola trebuie să conțină cel puțin %(min_length)d charactere.",
            self.min_length,
        ) % {"min_length": self.min_length}

class CPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Parolă veche'
        self.fields['new_password1'].label = 'Parolă nouă'
        self.fields['new_password2'].label = 'Confirmare parolă nouă'

        self.error_messages = {
        "password_incorrect": "Parola veche nu este corectă.",
        "password_mismatch": "Parolele nu coincid."
    }


class CPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Parolă nouă'
        self.fields['new_password2'].label = 'Confirmare parolă nouă'

        self.error_messages = {
        "password_mismatch": "Parolele nu coincid."
    }