from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.members.models import Employee
import uuid


User = get_user_model()


class MeetingType(models.Model):
    """
    Модель типа собрания
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название типа собрания')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип собрания'
        verbose_name_plural = 'Типы собраний'
        ordering = ['name']

    def __str__(self):
        return self.name


class Meeting(models.Model):
    """
    Модель собрания
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название собрания')
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.CASCADE, verbose_name='Тип собрания')
    agenda = models.TextField(verbose_name='Повестка дня')
    meeting_date = models.DateTimeField(verbose_name='Дата и время собрания')
    location = models.CharField(max_length=255, verbose_name='Место проведения')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Организатор')
    attendees = models.ManyToManyField(Employee, related_name='meetings_attended', verbose_name='Участники собрания')
    protocol = models.TextField(blank=True, verbose_name='Протокол собрания')
    is_published = models.BooleanField(default=False, verbose_name='Протокол опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Собрание'
        verbose_name_plural = 'Собрания'
        ordering = ['-meeting_date']

    def __str__(self):
        return f"{self.title} - {self.meeting_date.strftime('%d.%m.%Y')}"


class MotivatedOpinion(models.Model):
    """
    Модель мотивированного мнения
    """
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Подано'),
        ('reviewing', 'На рассмотрении'),
        ('approved', 'Утверждено'),
        ('rejected', 'Отклонено'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='motivated_opinions', verbose_name='Собрание')
    author = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание мотивированного мнения')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Мотивированное мнение'
        verbose_name_plural = 'Мотивированные мнения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.full_name}"


class DocumentSignature(models.Model):
    """
    Модель электронной подписи документа
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_type = models.CharField(max_length=50, verbose_name='Тип документа')
    document_id = models.UUIDField(verbose_name='ID документа')
    signer = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Подписавший')
    signature_hash = models.CharField(max_length=255, verbose_name='Хеш подписи')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время подписи')
    ip_address = models.GenericIPAddressField(verbose_name='IP-адрес', null=True, blank=True)

    class Meta:
        verbose_name = 'Электронная подпись'
        verbose_name_plural = 'Электронные подписи'
        unique_together = ['document_type', 'document_id', 'signer']

    def __str__(self):
        return f"Подпись {self.signer.full_name} для {self.document_type} {self.document_id}"