


from django.urls import path
from .views import index, create_email_account

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', create_email_account, name='accounts'),
]