from django.urls import path

from .views import CheckIn

urlpatterns = [
    path('check-in', CheckIn.as_view())
]