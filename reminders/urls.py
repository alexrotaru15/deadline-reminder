from django.urls import path
from . import views

app_name = 'reminders'
urlpatterns = [
    path('', views.home, name='home'),
]