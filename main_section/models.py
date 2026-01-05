from django.contrib.auth.models import User
from django.db import models

from manga_section.models import Chapter, Manga


class ChapterLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
                                related_name='likes')
    is_like = models.BooleanField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username}: {'Лайк' if self.is_like else 'Дизлайк'} главе {self.chapter.ch_name}"


class Profile(models.Model):
    THEME_CHOICES = [
        ('auto', 'Авто (по времени)'),
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='auto'
    )
    updated_at = models.DateTimeField(auto_now=True)
    viewed_tutorial = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.get_theme_display()}"


# Сигнал для автоматического создания профиля при создании пользователя
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ChapterView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
                                related_name='views')
    is_view = models.BooleanField(blank=True, null=True)
    view_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'chapter')