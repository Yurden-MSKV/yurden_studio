from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from post_section.models import Post, MessageFAQ


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ['post_name', 'post_slug', 'content', 'view_count']

@admin.register(MessageFAQ)
class MessageFAQAdmin(admin.ModelAdmin):
    list_display = ['author', 'message', 'created_at']