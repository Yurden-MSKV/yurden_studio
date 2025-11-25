import re
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.filter
def add_nbsp(value):
    if not value:
        return ""

    # Если значение уже помечено как safe, конвертируем в строку
    if hasattr(value, '__html__'):
        value = str(value)

    # Предлоги и союзы (неразрывный пробел ПОСЛЕ них)
    prepositions_conjunctions = r'в|во|на|над|под|за|из|от|до|по|о|об|обо|про|со|ко|изо|у|без|для|к|перед|при|через|сквозь|между|среди|вокруг|впереди|возле|мимо|вдоль|после|около|благодаря|ввиду|вследствие|вроде|наподобие|насчёт|включая|исключая|спустя|и|или|а|но|да|однако|зато|же|либо|то|не|то|ни|нибудь|либо|кое|ка|де|мол|будто|словно|точно|как|чем|нежели|чтоб|чтобы|ибо|потому|что|оттого|что|так|как|ли'

    # Частицы (неразрывный пробел ПЕРЕД ними)
    particles = r'ли|ль|неужели|разве|вот|вон|именно|прямо|точно|почти|единственно|только|лишь|исключительно|просто|хоть|хотя|бы|б|пусть|пускай|да|не|ни|нет|давай|давайте|ка|де|мол|дескать|скажем|положим|допустим|небось'

    patterns = [
        # Предлоги и союзы - неразрывный пробел ПОСЛЕ них
        (rf'\b({prepositions_conjunctions})\s+', r'\1&nbsp;'),

        # Частицы - неразрывный пробел ПЕРЕД ними
        (rf'\s+({particles})\b', r'&nbsp;\1'),

        # Тире - неразрывный пробел ПЕРЕД тире
        (r'\s+(—)', r'&nbsp;\1'),

        # Сокращения - неразрывный пробел ПОСЛЕ них
        (r'\b(г\.|№|стр\.|с\.|т\.|д\.|пр\.|ул\.|пер\.|бул\.|ш\.|наб\.|пл\.|ал\.|просп\.|б\-р)\s+', r'\1&nbsp;'),

        # Короткие слова (1-2 буквы) - неразрывный пробел ПОСЛЕ них
        (r'\b([а-яёa-z]{1,2})\s+', r'\1&nbsp;'),

        # Особый случай: "с другой" и подобные
        (r'\b(с)\s+(другой|тех|тех|тех|этой|той)\b', r'\1&nbsp;\2'),
        (r'\b(со)\s+(всей|всеми|мной|мною)\b', r'\1&nbsp;\2'),
    ]

    # Применяем все паттерны
    for pattern, replacement in patterns:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)

    return mark_safe(value)

@register.filter
def quote_break(text):
    count = 85
    soup = BeautifulSoup(text, 'html.parser')
    blockquotes = soup.find_all('blockquote')

    for blockquote in blockquotes:
        # Получаем текст внутри blockquote (без тегов)
        original_text = blockquote.get_text().strip()

        if len(original_text) <= count:
            # Если текст короткий, оставляем как есть
            continue
        else:
            # Разбиваем длинный текст на части
            words = original_text.split()
            lines = []
            current_line = []
            current_length = 0

            for word in words:
                # +1 учитывает пробел между словами
                if current_length + len(word) + 1 <= count or not current_line:
                    current_line.append(word)
                    current_length += len(word) + 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)

            if current_line:
                lines.append(' '.join(current_line))

            # Заменяем содержимое blockquote на разбитый текст
            blockquote.clear()
            for i, line in enumerate(lines):
                if i > 0:
                    blockquote.append(soup.new_tag('br'))
                blockquote.append(line)

    return mark_safe(str(soup))

@register.filter
def split_post_title(text, max_length=40):
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