from django import template

register = template.Library()

@register.filter
def reverse_list(value):
    """Переворачивает список"""
    return list(reversed(value))

@register.filter
def mod(value, arg):
    return value % arg