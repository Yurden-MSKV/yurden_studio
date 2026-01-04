from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from main_section.models import ChapterLike

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'date_joined']
    sortable_by = ('date_joined',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(ChapterLike)
class ChapterLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'chapter', 'is_like']