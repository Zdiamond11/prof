from django.db import models
from django.contrib.auth import get_user_model
from apps.members.models import Employee
import uuid


User = get_user_model()


class PaymentType(models.Model):
    """
    Модель типа выплаты
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название типа выплаты')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип выплаты'
        verbose_name_plural = 'Типы выплат'
        ordering = ['name']

    def __str__(self):
        return self.name


class MembershipFee(models.Model):
    """
    Модель членского взноса
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='membership_fees', verbose_name='Сотрудник')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма взноса')
    percentage_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент от зарплаты')
    period = models.DateField(verbose_name='Период (месяц/год)')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')
    paid_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплачено кем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Членский взнос'
        verbose_name_plural = 'Членские взносы'
        ordering = ['-period', 'employee__full_name']
        unique_together = ['employee', 'period']

    def __str__(self):
        return f"Взнос {self.employee.full_name} за {self.period.strftime('%m.%Y')}"

    @property
    def is_paid(self):
        """Проверяет, оплачен ли взнос"""
        return self.paid_at is not None


class FinancialSupportRequest(models.Model):
    """
    Модель заявки на выплату из фонда взаимопомощи
    """
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('reviewing', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('paid', 'Выплачена'),
        ('cancelled', 'Отменена'),
    ]

    SUPPORT_REASON_CHOICES = [
        ('material_aid', 'Материальная помощь'),
        ('child_birth', 'Рождение ребенка'),
        ('illness', 'Болезнь'),
        ('death', 'Смерть родственника'),
        ('other', 'Другое'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='support_requests', verbose_name='Сотрудник')
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заявитель')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Запрашиваемая сумма')
    reason = models.CharField(max_length=20, choices=SUPPORT_REASON_CHOICES, verbose_name='Причина выплаты')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    supporting_documents = models.FileField(upload_to='support_docs/', null=True, blank=True, verbose_name='Документы-основания')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests', verbose_name='Одобрено кем')
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата одобрения')
    payment_document = models.FileField(upload_to='payment_docs/', null=True, blank=True, verbose_name='Платежное поручение')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата выплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заявка на выплату'
        verbose_name_plural = 'Заявки на выплаты'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка {self.employee.full_name} - {self.get_reason_display()} ({self.amount})"


class FinancialRecord(models.Model):
    """
    Модель финансовой записи (доход/расход)
    """
    RECORD_TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES, verbose_name='Тип записи')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    description = models.TextField(verbose_name='Описание')
    related_request = models.ForeignKey(FinancialSupportRequest, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Связанная заявка')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создано кем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Финансовая запись'
        verbose_name_plural = 'Финансовые записи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_record_type_display()} {self.amount} - {self.description}"


class FinancialReport(models.Model):
    """
    Модель финансового отчета
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название отчета')
    period_start = models.DateField(verbose_name='Начало периода')
    period_end = models.DateField(verbose_name='Конец периода')
    content = models.TextField(verbose_name='Содержание отчета')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сформировано кем')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата формирования')
    file = models.FileField(upload_to='financial_reports/', null=True, blank=True, verbose_name='Файл отчета')

    class Meta:
        verbose_name = 'Финансовый отчет'
        verbose_name_plural = 'Финансовые отчеты'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} ({self.period_start.strftime('%d.%m.%Y')} - {self.period_end.strftime('%d.%m.%Y')})"