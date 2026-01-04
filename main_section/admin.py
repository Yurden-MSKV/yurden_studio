from django.contrib import admin

from main_section.models import ChapterLike


@admin.register(ChapterLike)
class ChapterLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'chapter', 'is_like']