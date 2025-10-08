from django.contrib.auth.models import User
from django.db import models

# Импортируем модель Post из вашего приложения
# ЗАМЕНИТЕ 'posts' на имя вашего приложения с постами!
from post_section.models import Post


class Poll(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='polls',
                             blank=True,
                             null=True)
    question = models.CharField(max_length=100)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             related_name='choices',
                             blank=True,
                             null=True,)
    choice_text = models.CharField(max_length=100,
                                   verbose_name='Варианты ответа')

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE,)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)

    def __str__(self):
        return self.choice.choice_text