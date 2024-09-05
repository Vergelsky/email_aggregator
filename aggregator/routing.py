from django.urls import path
from .consumers import EmailTableConsumer

ws_urlpatterns = [
    path('ws/email_table/', EmailTableConsumer.as_asgi()),
]