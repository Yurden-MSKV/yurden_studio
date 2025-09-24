from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):  # Более компактный вид
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'post', 'has_choices')
    list_filter = ('pub_date', 'post')
    search_fields = ('question_text',)
    list_editable = ('post',)  # Можно быстро менять привязку к посту из списка

    # Поле только для чтения - показывает есть ли варианты ответа
    def has_choices(self, obj):
        return obj.choices.exists()

    has_choices.boolean = True
    has_choices.short_description = 'Есть варианты'

    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes', 'related_post')

    # Показывает к какому посту привязан опрос
    def related_post(self, obj):
        return obj.question.post

    related_post.short_description = 'Пост'