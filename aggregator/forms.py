from django import forms

from config.settings import AVAILABLE_EMAIL_PROVIDERS
from .models import EmailAccount
from django.conf import settings

class EmailAccountForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(label='Пароль приложения', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    provider = forms.ChoiceField(label='Провайдер', choices=[], widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = EmailAccount
        fields = ['username', 'provider', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].choices = [(prov['url'], prov['name']) for prov in AVAILABLE_EMAIL_PROVIDERS]
