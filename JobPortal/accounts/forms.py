from django import forms
from .models import Gender_CHOICES, ROLE_CHOICES

class RegistrationForm(forms.Form):
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    gender = forms.ChoiceField(choices=Gender_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
