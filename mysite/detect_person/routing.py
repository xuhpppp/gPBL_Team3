from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/detect", consumers.DetectConsumer.as_asgi()),
]
