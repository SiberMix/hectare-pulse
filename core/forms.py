from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'inputGroup1'})  # сохраняем ваш класс для стилизации
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'inputGroup2'})  # сохраняем класс для пароля
    )
