from django.urls import path

from .views import UserRegister, UserLogin, CheckAdmin, UserLogout

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', UserRegister.as_view()),
    path('login', UserLogin.as_view(), name='login'),
    path('admin', CheckAdmin.as_view()),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', UserLogout.as_view())
]