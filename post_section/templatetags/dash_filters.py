import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def add_dash_nbsp(value):
    """Фильтр для замены пробелов перед тире на неразрывные"""
    if not value:
        return ""

    if hasattr(value, '__html__'):
        value = str(value)

    # Заменяем пробел перед любым тире на &nbsp;
    # Длинное тире —
    value = re.sub(r'\s+(—)', r'&nbsp;\1', value)
    # Короткое тире –
    value = re.sub(r'\s+(–)', r'&nbsp;\1', value)
    # Дефис - (если нужно)
    value = re.sub(r'\s+(-)\s+', r'&nbsp;— ', value)

    return mark_safe(value)