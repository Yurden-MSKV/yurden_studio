from django.db import models

# Импортируем модель Post из вашего приложения
# ЗАМЕНИТЕ 'posts' на имя вашего приложения с постами!
from post_section.models import Post


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Текст вопроса')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    # Связь с моделью Post. Опрос может быть привязан к конкретному посту.
    # null=True, blank=True позволяют создать опрос без привязки к посту.
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='polls',
                            null=True,
                            blank=True,
                            verbose_name='Прикрепленный пост'
                            )

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='choices')
    choice_text = models.CharField(max_length=200,
                                   verbose_name='Текст варианта ответа')
    votes = models.IntegerField(default=0,
                                editable=False,
                                verbose_name='Количество голосов')

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'