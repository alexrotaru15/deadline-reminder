from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from . import views

app_name = 'users'
urlpatterns = [
    path(
        'login/', 
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            authentication_form=AuthenticationForm, 
            next_page='reminders:home', 
            extra_context = dict(title='Login',),
            redirect_authenticated_user=True
            ), 
        name='login'
    ),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(
            next_page='reminders:home'
        ),
        name='logout'
    ),
    path(
        'register/', 
        views.register, 
        name='register'
    ),
    path(
        'password_change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html', 
            success_url=reverse_lazy('users:password_change_done')
        ), 
        name='password_change'
    ),
    path(
        'password_change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'password_reset', 
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html', 
            email_template_name='users/password_reset_email.html', 
            subject_template_name='users/password_reset_subject.txt',
            success_url=reverse_lazy('users:password_reset_done')
        ), 
        name='password_reset'
    ),
    path(
        'password_reset/done', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path(
        'password_reset/confirm/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ), 
        name='password_reset_confirm'
    ),
    path(
        'password_reset/complete', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ), 
        name='password_reset_complete'
    ),
    path(
        'profile/',
        views.profile,
        name='profile'
    )
]