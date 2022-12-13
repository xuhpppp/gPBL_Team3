from django.urls import path
from .views import Recognition
urlpatterns = [
    path('',Recognition.as_view())
]
