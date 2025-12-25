from django.db import models
from django.contrib.auth import get_user_model
from apps.members.models import Employee, Organization, Department
import uuid


User = get_user_model()


class ReportType(models.Model):
    """
    Модель типа отчета
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название типа отчета')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип отчета'
        verbose_name_plural = 'Типы отчетов'
        ordering = ['name']

    def __str__(self):
        return self.name


class MembershipReport(models.Model):
    """
    Модель отчета по членству
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название отчета')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    period_start = models.DateField(verbose_name='Начало периода')
    period_end = models.DateField(verbose_name='Конец периода')
    total_members = models.PositiveIntegerField(verbose_name='Всего членов')
    new_members = models.PositiveIntegerField(verbose_name='Вступило')
    left_members = models.PositiveIntegerField(verbose_name='Выбыло')
    membership_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент охвата (%)')
    content = models.TextField(verbose_name='Содержание отчета')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сформировано кем')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата формирования')
    file = models.FileField(upload_to='membership_reports/', null=True, blank=True, verbose_name='Файл отчета')

    class Meta:
        verbose_name = 'Отчет по членству'
        verbose_name_plural = 'Отчеты по членству'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} ({self.organization.name})"


class DemographicReport(models.Model):
    """
    Модель демографического отчета
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название отчета')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    period_start = models.DateField(verbose_name='Начало периода')
    period_end = models.DateField(verbose_name='Конец периода')
    content = models.TextField(verbose_name='Содержание отчета')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сформировано кем')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата формирования')
    file = models.FileField(upload_to='demographic_reports/', null=True, blank=True, verbose_name='Файл отчета')

    class Meta:
        verbose_name = 'Демографический отчет'
        verbose_name_plural = 'Демографические отчеты'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} ({self.organization.name})"


class MovementReport(models.Model):
    """
    Модель отчета по движению сотрудников
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название отчета')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Подразделение')
    period_start = models.DateField(verbose_name='Начало периода')
    period_end = models.DateField(verbose_name='Конец периода')
    arrived_employees = models.ManyToManyField(Employee, related_name='arrived_reports', verbose_name='Прибывшие')
    left_employees = models.ManyToManyField(Employee, related_name='left_reports', verbose_name='Уволенные')
    content = models.TextField(verbose_name='Содержание отчета')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сформировано кем')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата формирования')
    file = models.FileField(upload_to='movement_reports/', null=True, blank=True, verbose_name='Файл отчета')

    class Meta:
        verbose_name = 'Отчет по движению сотрудников'
        verbose_name_plural = 'Отчеты по движению сотрудников'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} ({self.department.name})"