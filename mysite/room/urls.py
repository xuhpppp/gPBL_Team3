from django.urls import path

from .views import OrderTask, OrderList

urlpatterns = [
    path('order', OrderTask.as_view()),
    path('order-list', OrderList.as_view())
]