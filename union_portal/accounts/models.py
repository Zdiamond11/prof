from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с ролями и профсоюзной информацией
    """
    USER_ROLES = (
        ('admin', 'Администратор'),
        ('chairman', 'Председатель профсоюза'),
        ('accountant', 'Бухгалтер'),
        ('organizer', 'Цеховой организатор'),
        ('member', 'Член профсоюза'),
    )

    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='member',
        verbose_name='Роль пользователя'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
    is_2fa_enabled = models.BooleanField(
        default=False,
        verbose_name='Двухфакторная аутентификация включена'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Organization(models.Model):
    """
    Модель организации/подразделения
    """
    name = models.CharField(max_length=255, verbose_name='Название организации')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Родительская организация'
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'