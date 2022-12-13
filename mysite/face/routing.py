from django.urls import path

from .consumers import RecognizeConsumer, InsertConsumer

ws_urlpatterns = [
    path('ws/some_url', RecognizeConsumer.as_asgi()),
    path('ws/insert', InsertConsumer.as_asgi())
]