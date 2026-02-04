from django import forms

from manga_section.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Твой комментарий',
                'class': 'comment_area',
                'rows': 4
            }),
        }