from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from datetime import date
import uuid


class Organization(models.Model):
    """
    Модель организации
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Название организации')
    short_name = models.CharField(max_length=100, verbose_name='Краткое название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    """
    Модель подразделения/цеха
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments', verbose_name='Организация')
    name = models.CharField(max_length=255, verbose_name='Название подразделения')
    short_name = models.CharField(max_length=100, verbose_name='Краткое название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.organization.short_name})"


class EducationLevel(models.Model):
    """
    Модель уровня образования
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Уровень образования')

    class Meta:
        verbose_name = 'Уровень образования'
        verbose_name_plural = 'Уровни образования'
        ordering = ['name']

    def __str__(self):
        return self.name


class Position(models.Model):
    """
    Модель должности
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Название должности')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']

    def __str__(self):
        return self.name


class EmploymentHistory(models.Model):
    """
    Модель трудовой истории
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employment_history')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    appointment_date = models.DateField(verbose_name='Дата назначения')
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Ставка (в %)')
    is_main_position = models.BooleanField(default=False, verbose_name='Основная должность')
    employment_start_date = models.DateField(verbose_name='Дата приема на работу')
    employment_end_date = models.DateField(null=True, blank=True, verbose_name='Дата увольнения')

    class Meta:
        verbose_name = 'Трудовая история'
        verbose_name_plural = 'Трудовая история'
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.position.name} - {self.employee.full_name}"


class Employee(models.Model):
    """
    Модель сотрудника
    """
    MARITAL_STATUS_CHOICES = [
        ('single', 'Не женат/Не замужем'),
        ('married', 'Женат/Замужем'),
        ('divorced', 'Разведен(а)'),
        ('widowed', 'Вдовец/Вдова'),
    ]

    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('inactive', 'Выбыл'),
        ('retired', 'На пенсии'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', verbose_name='Подразделение')
    employee_number = models.CharField(max_length=50, unique=True, verbose_name='Табельный номер')
    full_name = models.CharField(max_length=255, verbose_name='ФИО (полное)')
    short_name = models.CharField(max_length=100, verbose_name='ФИО (сокращенное)')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, verbose_name='Семейное положение')
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Уровень образования')
    education_institution = models.CharField(max_length=255, blank=True, verbose_name='Учебное заведение')
    education_graduation_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Год окончания')
    passport_series = models.CharField(max_length=10, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=20, verbose_name='Номер паспорта')
    passport_issue_date = models.DateField(verbose_name='Дата выдачи паспорта')
    passport_issued_by = models.CharField(max_length=255, verbose_name='Кем выдан')
    registration_address = models.TextField(verbose_name='Адрес регистрации')
    passport_scan = models.FileField(upload_to='passports/', null=True, blank=True, verbose_name='Скан паспорта')
    union_ticket_number = models.CharField(max_length=50, unique=True, verbose_name='Номер профсоюзного билета')
    union_join_date = models.DateField(verbose_name='Дата вступления в профсоюз')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.employee_number})"

    @property
    def age(self):
        """Вычисляет возраст сотрудника"""
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def current_position(self):
        """Возвращает текущую должность сотрудника"""
        current_history = self.employment_history.filter(employment_end_date__isnull=True).first()
        if current_history:
            return current_history.position
        return None


class Child(models.Model):
    """
    Модель ребенка сотрудника
    """
    DISABILITY_STATUS_CHOICES = [
        ('none', 'Нет'),
        ('disability', 'Инвалидность'),
        ('multichild', 'Многодетный'),
        ('other', 'Другое'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='children', verbose_name='Сотрудник')
    full_name = models.CharField(max_length=255, verbose_name='ФИО ребенка')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    disability_status = models.CharField(max_length=20, choices=DISABILITY_STATUS_CHOICES, default='none', verbose_name='Льготная категория')

    class Meta:
        verbose_name = 'Ребенок сотрудника'
        verbose_name_plural = 'Дети сотрудников'
        ordering = ['date_of_birth']

    def __str__(self):
        return f"{self.full_name} ({self.employee.full_name})"

    @property
    def age(self):
        """Вычисляет возраст ребенка"""
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))