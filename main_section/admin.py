from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from main_section.models import ChapterLike, ChapterView, Profile


class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'date_joined']
    # sortable_by = ('date_joined',)
    ordering = ('-date_joined',)
    list_per_page = 100
    search_fields = ['username']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(ChapterLike)
class ChapterLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'manga', 'chapter', 'is_like', 'created_at']
    # list_per_page = 10
    readonly_fields = ['created_at']

class UserFilter(AutocompleteFilter):
    title = 'Пользователь'
    field_name = 'user'

@admin.register(ChapterView)
class ChapterViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'manga', 'chapter', 'view_date']
    ordering = ('-view_date',)
    list_per_page = 50
    list_filter = (UserFilter,)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'viewed_single', 'viewed_double', 'reader_mode']
    save_on_top = True