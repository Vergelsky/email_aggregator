from django.db import models
from config.settings import AVAILABLE_EMAIL_PROVIDERS

NULLABLE = {'null': True, 'blank': True}


class EmailAccount(models.Model):
    PROVIDER_CHOICES = tuple((provider['url'], provider['name']) for provider in AVAILABLE_EMAIL_PROVIDERS)

    email = models.EmailField(unique=True, verbose_name='Адрес')
    password = models.CharField(max_length=35, verbose_name='Пароль')
    provider = models.CharField(choices=PROVIDER_CHOICES, max_length=250, verbose_name='Адрес электронной почты')

    class Meta:
        verbose_name = 'Аккаунт электронной почты'
        verbose_name_plural = 'Аккаунты электронной почты'


class EmailMessage(models.Model):
    account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, verbose_name='Аккаунт')
    subject = models.CharField(max_length=255, verbose_name='Тема', **NULLABLE)
    sent_date = models.DateTimeField(verbose_name='Дата отправки')
    received_date = models.DateTimeField(verbose_name='Дата получения')
    body = models.TextField(max_length=5000, verbose_name='Текст письма', **NULLABLE)
    attachments = models.FileField(upload_to='attachments', verbose_name='Вложения', **NULLABLE)

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
