from django.urls import path
from . import views

app_name = 'reminders'
urlpatterns = [
    path('', views.home, name='home'),
    path('add_reminder/', views.add_reminder, name='add_reminder'),
    path('reminders/', views.RemindersView.as_view(), name='reminders_list'),
    path('reminders/delete/<reminder_id>', views.delete_reminder, name='delete_reminder')
]
