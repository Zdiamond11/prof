from django.db import models
from django.contrib.auth import get_user_model
from apps.members.models import Organization
import uuid


User = get_user_model()


class DashboardWidget(models.Model):
    """
    Модель виджета дашборда
    """
    WIDGET_TYPE_CHOICES = [
        ('membership_stats', 'Статистика по членству'),
        ('finance_stats', 'Финансовая статистика'),
        ('voting_stats', 'Статистика голосований'),
        ('news_feed', 'Лента новостей'),
        ('recent_activity', 'Недавняя активность'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Название виджета')
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPE_CHOICES, verbose_name='Тип виджета')
    title = models.CharField(max_length=255, verbose_name='Заголовок виджета')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.PositiveIntegerField(verbose_name='Порядок отображения')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Виджет дашборда'
        verbose_name_plural = 'Виджеты дашборда'
        ordering = ['order']

    def __str__(self):
        return self.name


class DashboardConfiguration(models.Model):
    """
    Модель конфигурации дашборда для пользователя
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_config', verbose_name='Пользователь')
    widgets = models.ManyToManyField(DashboardWidget, through='UserDashboardWidget', verbose_name='Виджеты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Конфигурация дашборда'
        verbose_name_plural = 'Конфигурации дашбордов'

    def __str__(self):
        return f"Конфигурация дашборда {self.user.username}"


class UserDashboardWidget(models.Model):
    """
    Модель связи пользователя с виджетом дашборда
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE, verbose_name='Виджет')
    position_x = models.PositiveIntegerField(verbose_name='Позиция X')
    position_y = models.PositiveIntegerField(verbose_name='Позиция Y')
    width = models.PositiveIntegerField(verbose_name='Ширина')
    height = models.PositiveIntegerField(verbose_name='Высота')
    is_visible = models.BooleanField(default=True, verbose_name='Видимый')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Связь пользователя и виджета дашборда'
        verbose_name_plural = 'Связи пользователей и виджетов дашборда'
        unique_together = ['user', 'widget']

    def __str__(self):
        return f"{self.user.username} - {self.widget.name}"


class KeyPerformanceIndicator(models.Model):
    """
    Модель ключевого показателя эффективности
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Название KPI')
    description = models.TextField(verbose_name='Описание')
    value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Значение')
    target_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Целевое значение')
    unit = models.CharField(max_length=20, verbose_name='Единица измерения')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    period = models.DateField(verbose_name='Период')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Ключевой показатель эффективности'
        verbose_name_plural = 'Ключевые показатели эффективности'
        ordering = ['-period', 'name']

    def __str__(self):
        return f"{self.name} - {self.period.strftime('%m.%Y')}"

    @property
    def is_target_achieved(self):
        """Проверяет, достигнуто ли целевое значение"""
        return self.value >= self.target_value