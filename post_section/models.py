from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import re

class Tag(models.Model):
    tag_name = models.CharField(max_length=50,
                                verbose_name='Название')

    def __str__(self):
        return self.tag_name

class Post(models.Model):
    post_name = models.CharField(max_length=150,
                                 verbose_name='Название')
    post_slug = models.SlugField(max_length=200,
                                 unique=True,
                                 verbose_name='SLUG-адрес')
    tags = models.ManyToManyField(Tag,
                                  related_name='posts',
                                  verbose_name='Теги')
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
    author = models.ForeignKey(User,
                               on_delete=models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Предложение от {self.author.username}"

    class Meta:
        verbose_name = 'Предложения'
        verbose_name_plural = 'Предложения'


class Thread(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='threads',
                             verbose_name='Пост')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Ветки'
        verbose_name_plural = 'Ветки'


class PostComment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост',
                             default=None,
                             blank=True,
                             null=True)
    author = models.ForeignKey(User,
                               on_delete=models.DO_NOTHING,
                               related_name='post_comments',
                               verbose_name='Автор')
    thread = models.ForeignKey(Thread,
                               on_delete=models.CASCADE,
                               default=None,
                               blank=True,
                               null=True,
                               related_name='comments',
                               verbose_name='Ветка')
    parent_comment = models.ManyToManyField('post_section.PostComment',
                                            verbose_name='Родитель',
                                            default=None,
                                            blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    def __str__(self):
        return f"{self.author}: {self.text}"

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'