from django import template
from django.utils.safestring import mark_safe

register = template.Library()




@register.filter
def smart_break(text):
    count = 37

    """Разбивает текст перед словом, если символов > 40"""
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