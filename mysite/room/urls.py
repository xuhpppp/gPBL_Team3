from django.urls import path

from .views import OrderTask

urlpatterns = [
    path('order/', OrderTask.as_view())
]