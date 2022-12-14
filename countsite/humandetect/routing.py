from django.urls import path

from .consumers import CountConsumer

ws_urlpatterns = [
    path('ws/count', CountConsumer.as_asgi())
]