from django import forms

from post_section.models import MessageFAQ


class FAQform(forms.ModelForm):
    # message = forms.CharField(label='Твоё предложение:', max_length=1000)

    class Meta:
        model = MessageFAQ
        fields = ['message']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }