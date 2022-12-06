from django.urls import path
from .views import webcam_stream,index


urlpatterns = [
    path('', webcam_stream),
    path('view/', index),
]
