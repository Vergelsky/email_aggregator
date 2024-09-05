from django.shortcuts import render, redirect
from django.urls import reverse

from aggregator.forms import EmailAccountForm
from aggregator.models import EmailAccount
from config.settings import AVAILABLE_EMAIL_PROVIDERS


# Create your views here.
def index(request):
    return render(request, 'index.html', context={'text': 'Hello, World!'})


def create_email_account(request):
    if request.method == 'POST':
        form = EmailAccountForm(request.POST, provider_choices=AVAILABLE_EMAIL_PROVIDERS)
        if form.is_valid():
            # Создаем новый объект EmailAccount
            email_account = EmailAccount(
                email=f"{form.cleaned_data['username']}@{form.cleaned_data['provider']}",
                password=form.cleaned_data['password'],
                provider=form.cleaned_data['provider']
            )
            email_account.save()
            return redirect(reverse('index'))
    else:
        form = EmailAccountForm(provider_choices=AVAILABLE_EMAIL_PROVIDERS)

    return render(request, 'form.html', {'form': form, 'providers': AVAILABLE_EMAIL_PROVIDERS})
