# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts 
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
   
    # Reset Password
    path('accounts/password/reset/', CustomPasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('accounts/reset/password/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

]