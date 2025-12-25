from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid


User = get_user_model()


class NewsCategory(models.Model):
    """
    Модель категории новостей
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория новостей'
        verbose_name_plural = 'Категории новостей'
        ordering = ['name']

    def __str__(self):
        return self.name


class NewsPost(models.Model):
    """
    Модель новости
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name='Категория')
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплена')
    published_at = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель комментария к новости
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news_post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='comments', verbose_name='Новость')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    content = models.TextField(verbose_name='Содержание комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.news_post.title}'