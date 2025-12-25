from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Аутентификация и авторизация
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    # Двухфакторная аутентификация
    path('two-factor/setup/', views.TwoFactorSetupView.as_view(), name='two_factor_setup'),
    path('two-factor/verify/', views.TwoFactorVerifyView.as_view(), name='two_factor_verify'),
]