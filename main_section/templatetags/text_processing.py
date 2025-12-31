import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def smart_break(text, request=None):

    home_count = 23
    manga_count = 50
    count = manga_count

    # Если передан request, определяем путь
    if request and hasattr(request, 'path'):
        current_path = request.path
        if current_path.startswith('/home/'):
            count = home_count
        elif current_path.startswith('/manga/'):
            count = manga_count

    """Разбивает текст перед словом, если символов > count"""
    if not text:
        return ''

    original_text = str(text).strip()

    # Если текст короткий - возвращаем как есть
    if len(original_text) <= count:
        return original_text

    words = original_text.split()

    # Ищем перед каким словом поставить перенос
    current_position = 0

    for i, word in enumerate(words):
        # Находим позицию текущего слова в тексте
        word_position = original_text.find(word, current_position)
        if word_position == -1:
            continue

        # Если позиция начала слова превышает 40 символов и это не первое слово
        if word_position > count and i > 0:
            # Ставим перенос перед этим словом
            break_position = word_position
            first_line = original_text[:break_position].strip()
            second_line = original_text[break_position:].strip()
            return mark_safe(f'{first_line}<br>{second_line}')

        current_position = word_position + len(word)

    # Если не нашли подходящего места, разбиваем по последнему пробелу до 40 символов
    last_space_before_40 = original_text.rfind(' ', 0, count)
    if last_space_before_40 != -1:
        first_line = original_text[:last_space_before_40].strip()
        second_line = original_text[last_space_before_40:].strip()
        return mark_safe(f'{first_line}<br>{second_line}')

    # Если нет пробелов вообще, оставляем как есть
    return original_text

@register.filter
def smart_break_mobile(text, request=None):

    home_count = 23
    manga_count = 23
    count = manga_count

    # Если передан request, определяем путь
    if request and hasattr(request, 'path'):
        current_path = request.path
        if current_path.startswith('/home/'):
            count = home_count
        elif current_path.startswith('/manga/'):
            count = manga_count

    """Разбивает текст перед словом, если символов > count"""
    if not text:
        return ''

    original_text = str(text).strip()

    # Если текст короткий - возвращаем как есть
    if len(original_text) <= count:
        return original_text

    words = original_text.split()

    # Ищем перед каким словом поставить перенос
    current_position = 0

    for i, word in enumerate(words):
        # Находим позицию текущего слова в тексте
        word_position = original_text.find(word, current_position)
        if word_position == -1:
            continue

        # Если позиция начала слова превышает 40 символов и это не первое слово
        if word_position > count and i > 0:
            # Ставим перенос перед этим словом
            break_position = word_position
            first_line = original_text[:break_position].strip()
            second_line = original_text[break_position:].strip()
            return mark_safe(f'{first_line}<br>{second_line}')

        current_position = word_position + len(word)

    # Если не нашли подходящего места, разбиваем по последнему пробелу до 40 символов
    last_space_before_40 = original_text.rfind(' ', 0, count)
    if last_space_before_40 != -1:
        first_line = original_text[:last_space_before_40].strip()
        second_line = original_text[last_space_before_40:].strip()
        return mark_safe(f'{first_line}<br>{second_line}')

    # Если нет пробелов вообще, оставляем как есть
    return original_text


@register.filter
def split_by_width_ignore_html(text, max_length=23):
    """Разбивает текст на строки, игнорируя HTML-сущности при подсчёте длины"""
    if hasattr(text, '__html__'):
        text = str(text)

    words = text.split()
    lines = []
    current_line = []
    current_visual_length = 0

    for word in words:
        # Убираем HTML-сущности для подсчёта длины, но сохраняем их в вывод
        clean_word = re.sub(r'&[^;]+;', '', word)
        word_visual_length = len(clean_word)

        # Учитываем пробел между словами
        space_length = 1 if current_line else 0

        if current_visual_length + space_length + word_visual_length > max_length:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_visual_length = 0
                space_length = 0  # После сброса строки пробел не нужен

        current_line.append(word)
        current_visual_length += space_length + word_visual_length

    if current_line:
        lines.append(' '.join(current_line))

    # Сохраняем HTML-безопасный вывод
    return mark_safe('<br>'.join(lines))