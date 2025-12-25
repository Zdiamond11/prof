from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.members.models import Employee, Department
import uuid


User = get_user_model()


class VotingType(models.Model):
    """
    Модель типа голосования
    """
    VOTING_TYPE_CHOICES = [
        ('open', 'Открытое'),
        ('anonymous', 'Анонимное'),
        ('quorum', 'Голосование кворума'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название типа голосования')
    type = models.CharField(max_length=20, choices=VOTING_TYPE_CHOICES, verbose_name='Тип голосования')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип голосования'
        verbose_name_plural = 'Типы голосований'
        ordering = ['name']

    def __str__(self):
        return self.name


class VoteOption(models.Model):
    """
    Модель варианта ответа в голосовании
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voting = models.ForeignKey('Voting', on_delete=models.CASCADE, related_name='options', verbose_name='Голосование')
    text = models.CharField(max_length=255, verbose_name='Текст варианта ответа')
    order = models.PositiveIntegerField(verbose_name='Порядок')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['order']

    def __str__(self):
        return f"{self.text} (Голосование: {self.voting.title})"


class Voting(models.Model):
    """
    Модель голосования
    """
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активно'),
        ('closed', 'Завершено'),
    ]

    VOTE_TYPE_CHOICES = [
        ('single', 'Один выбор'),
        ('multiple', 'Множественный выбор'),
        ('scale', 'Шкала оценок'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название голосования')
    description = models.TextField(verbose_name='Описание')
    voting_type = models.ForeignKey(VotingType, on_delete=models.CASCADE, verbose_name='Тип голосования')
    vote_type = models.CharField(max_length=20, choices=VOTE_TYPE_CHOICES, default='single', verbose_name='Тип голоса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    target_audience = models.ManyToManyField(Department, blank=True, verbose_name='Целевая аудитория')
    quorum_required = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Требуемый кворум (%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        """Проверяет, активно ли голосование"""
        now = timezone.now()
        return self.status == 'active' and self.start_date <= now and self.end_date >= now

    def get_participants_count(self):
        """Возвращает количество участников голосования"""
        if self.target_audience.exists():
            # Если указана целевая аудитория (подразделения), считаем сотрудников этих подразделений
            return Employee.objects.filter(department__in=self.target_audience.all()).count()
        else:
            # Иначе считаем всех сотрудников
            return Employee.objects.count()

    def get_votes_count(self):
        """Возвращает количество отданных голосов"""
        return self.votes.count()


class Vote(models.Model):
    """
    Модель голоса
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='votes', verbose_name='Голосование')
    voter = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Голосующий')
    selected_options = models.ManyToManyField(VoteOption, verbose_name='Выбранные варианты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата голосования')
    ip_address = models.GenericIPAddressField(verbose_name='IP-адрес', null=True, blank=True)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = ['voting', 'voter']

    def __str__(self):
        return f"Голос {self.voter.full_name} в {self.voting.title}"


class QuorumVotingResult(models.Model):
    """
    Модель результата голосования кворума
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voting = models.OneToOneField(Voting, on_delete=models.CASCADE, related_name='quorum_result', verbose_name='Голосование')
    quorum_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент кворума')
    total_voters = models.PositiveIntegerField(verbose_name='Всего проголосовало')
    required_voters = models.PositiveIntegerField(verbose_name='Требуется проголосовать')
    is_quorum_reached = models.BooleanField(verbose_name='Кворум достигнут')
    decision_made = models.BooleanField(verbose_name='Решение принято')
    decision_description = models.TextField(verbose_name='Описание решения', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Результат голосования кворума'
        verbose_name_plural = 'Результаты голосований кворума'

    def __str__(self):
        return f"Результат кворума: {self.voting.title}"