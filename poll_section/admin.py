from django.contrib import admin
from .models import Poll, Choice


class ChoiceInline(admin.TabularInline):  # Более компактный вид
    model = Choice
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('post', 'question')

    # Поле только для чтения - показывает есть ли варианты ответа
    def has_choices(self, obj):
        return obj.choices.exists()

    has_choices.boolean = True
    has_choices.short_description = 'Есть варианты'

    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice_text')

    # Показывает к какому посту привязан опрос
    def related_post(self, obj):
        return obj.question.post

    related_post.short_description = 'Пост'