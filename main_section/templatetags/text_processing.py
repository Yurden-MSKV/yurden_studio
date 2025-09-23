from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def smart_break(text):
    """Простая версия с четкой логикой"""
    if not text:
        return ''

    text = str(text).strip()
    words = text.split()

    if len(text) > 42:
        # Ищем перед каким словом ставить перенос
        length_so_far = 0
        for i in range(len(words)):
            length_so_far += len(words[i]) + (1 if i > 0 else 0)

            # Если превысили 42 символов и это не первое слово
            if length_so_far > 42 and i > 0:
                return mark_safe(' '.join(words[:i]) + '<br>' + ' '.join(words[i:]))

    # Условия для переноса
    if len(words) > 4:
        # Перенос после 4-го слова
        return mark_safe(' '.join(words[:4]) + '<br>' + ' '.join(words[4:]))



    return text