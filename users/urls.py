from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from . import views
from .views import CLoginView, CPasswordResetConfirmView
from .forms import CPasswordChangeForm, CPasswordResetConfirmForm

app_name = 'users'
urlpatterns = [
    path(
        'login/', 
        CLoginView.as_view(
            template_name='users/login.html',
            authentication_form=AuthenticationForm, 
            next_page='reminders:home', 
            extra_context = dict(title='Autentificare',),
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
            form_class=CPasswordChangeForm,
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
        CPasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:login'),
            form_class=CPasswordResetConfirmForm
        ), 
        name='password_reset_confirm'
    ),
    path(
        'profile/',
        views.profile,
        name='profile'
    )
]