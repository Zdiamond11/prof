from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings
import uuid


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с профсоюзными данными
    """
    USER_ROLES = [
        ('admin', 'Администратор'),
        ('chairman', 'Председатель профсоюза'),
        ('accountant', 'Бухгалтер'),
        ('organizer', 'Цеховой организатор'),
        ('member', 'Член профсоюза'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='member', verbose_name='Роль')
    organization = models.ForeignKey('members.Organization', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Организация')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class UserProfile(models.Model):
    """
    Профиль пользователя с дополнительной информацией
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Телефонный номер должен быть в формате: '+999999999'. До 15 цифр.")],
        blank=True,
        verbose_name='Номер телефона'
    )
    email_confirmed = models.BooleanField(default=False, verbose_name='Email подтвержден')
    two_factor_enabled = models.BooleanField(default=False, verbose_name='Двухфакторная аутентификация включена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль {self.user.username}"