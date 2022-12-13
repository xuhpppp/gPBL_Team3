from django.urls import path

from .views import OrderTask, OrderList, OrderDetail, StaffList

urlpatterns = [
    path('order', OrderTask.as_view()),
    path('order/<str:pk>', OrderTask.as_view()),
    path('order-list', OrderList.as_view()),
    path('order-detail/<str:pk>', OrderDetail.as_view()),
    path('staff-order/<str:pk>', StaffList.as_view())
]