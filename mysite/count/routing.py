from django.urls import path

from .consumers import Counting

ws_urlpatterns = [
    path('ws/count', Counting.as_asgi())
]