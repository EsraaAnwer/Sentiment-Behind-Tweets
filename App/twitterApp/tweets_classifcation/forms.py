from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact_us


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class Contact_us_form(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = ['first_name', 'mail', 'phonenumber', 'message']