from django.urls import path
from . import views
from .views import ListPersonView
urlpatterns = [
    path('', views.ListPersonView.as_view(), name='API to get list of person'),
    path('<int:khoachinh>', ListPersonView.as_view())
]