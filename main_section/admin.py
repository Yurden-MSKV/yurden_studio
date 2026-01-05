from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from main_section.models import ChapterLike, ChapterView, Profile


class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'date_joined']
    # sortable_by = ('date_joined',)
    ordering = ('-date_joined',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(ChapterLike)
class ChapterLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'chapter', 'is_like']

@admin.register(ChapterView)
class ChapterViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'manga', 'chapter', 'view_date']
    ordering = ('-view_date',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'viewed_tutorial']