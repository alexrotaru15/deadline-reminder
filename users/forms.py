from distutils.command.clean import clean
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from phonenumber_field.formfields import PhoneNumberField


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
