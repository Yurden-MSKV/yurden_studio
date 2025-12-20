from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import re


class Post(models.Model):
    post_name = models.CharField(max_length=150,
                                 verbose_name='Название')
    post_slug = models.SlugField(max_length=200,
                                 unique=True,
                                 verbose_name='SLUG-адрес')
    content = RichTextUploadingField(verbose_name='Содержание')
    add_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время создания')
    view_count = models.PositiveIntegerField(default=0,
                                             editable=False,
                                             verbose_name='Счётчик просмотров')
    visibility = models.BooleanField(default=True,
                                     verbose_name='Отображение на главной')

    def __str__(self):
        return self.post_name

    def get_short_content(self, max_length=155):
        """
        Возвращает укороченное содержимое без изображений и с заменой &nbsp; на пробелы
        """
        # Удаляем все теги img
        content_no_images = re.sub(r'<img[^>]*>', '', self.content)

        # Заменяем &nbsp; на обычные пробелы
        content_no_nbsp = re.sub(r'&nbsp;', ' ', content_no_images)

        # Получаем чистый текст
        text_only = re.sub(r'<[^>]*>', '', content_no_nbsp)

        # Обрезаем текст
        if len(text_only) > max_length:
            return text_only[:max_length] + '...'
        return text_only

    def get_short_content_safe(self, max_length=155):
        """
        Безопасная версия для использования в шаблонах
        """
        from django.utils.safestring import mark_safe
        return mark_safe(self.get_short_content(max_length))

    def short_for_catalog(self, max_length=250):
        from django.utils.safestring import mark_safe
        return mark_safe(self.get_short_content(max_length))

class MessageFAQ(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Предложение от {self.author.username}"

    def messages_count(self):
        return MessageFAQ.objects.filter(is_read=False).count()

    class Meta:
        verbose_name = 'Предложения'
        verbose_name_plural  = 'Предложения'