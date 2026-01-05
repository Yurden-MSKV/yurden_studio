from django.http import Http404, JsonResponse
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from main_section.views import message_count
from manga_section.models import Manga, Chapter, ChapterImage
from main_section.models import ChapterLike, ChapterView

from django.shortcuts import render, get_object_or_404


def catalog_page(request):
    manga_list = Manga.objects.all()

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    context = {
        'manga_list': manga_list,
        'messages_cnt': message_cnt,
    }

    return render(request, "catalog_page.html", context)

def manga_page(request, slug):
    # Получаем мангу с предзагрузкой всех связанных данных
    manga = get_object_or_404(Manga.objects.prefetch_related(
        'volumes__chapters__likes',  # Тома и их главы
        'volumes__chapters__views',
        'genres',
        'authors'
    ), manga_slug=slug)

    # Получаем тома, отсортированные по номеру
    volumes = manga.volumes.all().order_by('vol_number')

    viewed_chapters_dates = list(ChapterView.objects.filter(
        user=request.user,
        manga=manga,
        is_view=True
    ).order_by('view_date').values_list('chapter_id', flat=True))

    viewed_chapters = set(viewed_chapters_dates)

    genres = manga.genres.all()
    authors = manga.authors.all()

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    context = {
        'manga': manga,
        'volumes': volumes,  # Добавляем тома в контекст
        'genres': genres,
        'authors': authors,
        'viewed_chapters_dates': viewed_chapters_dates,
        'viewed_chapters': viewed_chapters,
        'messages_cnt': message_cnt,
    }
    return render(request, 'manga_page.html', context)


@ensure_csrf_cookie
def chapter_page(request, manga_slug, ch_number):

    # Ищем мангу по slug
    manga = get_object_or_404(Manga, manga_slug=manga_slug)

    # Преобразуем chapter_number в Decimal для поиска
    try:
        chapter_number_decimal = Decimal(ch_number)
    except:
        raise Http404("Неверный формат номера главы")

    chapter = get_object_or_404(
        Chapter.objects.filter(volume__manga=manga),
        ch_number=ch_number
    )

    chapter_view, created = ChapterView.objects.update_or_create(
        user=request.user,
        chapter=chapter,
        manga=manga,
        defaults={
            'is_view': True,
            'view_date': timezone.now()  # Всегда обновляем дату
        }
    )

    prev_chapter = Chapter.objects.filter(
        volume__manga=manga,
        ch_number__lt=ch_number
    ).order_by('-ch_number').first()
    if prev_chapter:
        print(f"Предыдушая глава: {prev_chapter.get_chapter_display()}")
    else:
        print("Предыдущей нет.")

    # Следующая глава (минимальный номер больше текущего)
    next_chapter = Chapter.objects.filter(
        volume__manga=manga,
        ch_number__gt=ch_number
    ).order_by('ch_number').first()
    if next_chapter:
        print(f"Следующая глава: {next_chapter.get_chapter_display()}")
    else:
        print("Следующей нет.")

    images = ChapterImage.objects.filter(chapter=chapter).order_by('page_number')

    # Функция для создания пар с учетом разворотов
    def create_page_pairs(images):
        pairs = []
        i = 0
        while i < len(images):
            current_page = images[i]

            # Если текущая страница - разворот
            if current_page.is_double_page or current_page.page_number == 1:
                pairs.append([current_page])  # Добавляем как одиночный элемент
                i += 1
                continue

            # Если следующая страница существует и не является разворотом
            if i + 1 < len(images) and not images[i + 1].is_double_page:
                pairs.append([current_page, images[i + 1]])
                i += 2
            else:
                # Если следующая страница - разворот или последняя страница
                pairs.append([current_page])
                i += 1

        return pairs

    def page_mobile(images):
        pages = []
        i = 0
        while i < len(images):
            if not images[i].is_placeholder:
                pages.append(images[i])
                i += 1
            else:
                i += 1
                continue


        return pages

    if request.is_mobile:
        page_pairs = page_mobile(images)
    else:
        page_pairs = create_page_pairs(images)

    # Получаем статистику оценок
    likes_count = ChapterLike.objects.filter(chapter=chapter, is_like=True).count()
    dislikes_count = ChapterLike.objects.filter(chapter=chapter, is_like=False).count()
    total_ratings = likes_count + dislikes_count

    if total_ratings > 0:
        like_percentage = round((likes_count / total_ratings) * 100)
    else:
        like_percentage = 0

    # Проверяем оценку текущего пользователя
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_like = ChapterLike.objects.get(user=request.user, chapter=chapter)
            user_rating = 'like' if user_like.is_like else 'dislike'
        except ChapterLike.DoesNotExist:
            pass

    context = {
        'manga': manga,
        'chapter': chapter,
        'images': images,
        'page_pairs': page_pairs,
        'like_percentage': like_percentage,
        'user_rating': user_rating,
        'prev_chapter': prev_chapter.get_chapter_display if prev_chapter else None,
        'next_chapter': next_chapter.get_chapter_display if next_chapter else None,
    }
    return render(request, 'chapter_page.html', context)


@login_required
@require_POST
def rate_chapter(request, manga_slug, ch_number):
    """Обработка оценки главы"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)

    manga = get_object_or_404(Manga, manga_slug=manga_slug)

    try:
        chapter = Chapter.objects.get(
            volume__manga=manga,
            ch_number=ch_number
        )
    except Chapter.DoesNotExist:
        return JsonResponse({'error': 'Глава не найдена'}, status=404)

    is_like = request.POST.get('is_like')
    if is_like is None:
        return JsonResponse({'error': 'Не указан тип оценки'}, status=400)

    is_like = is_like.lower() == 'true'

    # Проверяем, есть ли уже оценка от пользователя
    try:
        existing_like = ChapterLike.objects.get(user=request.user, chapter=chapter)

        # Если пользователь нажимает на ту же кнопку - удаляем оценку
        if existing_like.is_like == is_like:
            existing_like.delete()
            user_rating = None
        else:
            # Если нажимает на другую кнопку - меняем оценку
            existing_like.is_like = is_like
            existing_like.save()
            user_rating = 'like' if is_like else 'dislike'

    except ChapterLike.DoesNotExist:
        # Если оценки нет - создаем новую
        ChapterLike.objects.create(
            user=request.user,
            chapter=chapter,
            is_like=is_like
        )
        user_rating = 'like' if is_like else 'dislike'

    # Получаем обновленную статистику оценок
    likes_count = ChapterLike.objects.filter(chapter=chapter, is_like=True).count()
    dislikes_count = ChapterLike.objects.filter(chapter=chapter, is_like=False).count()
    total_ratings = likes_count + dislikes_count

    if total_ratings > 0:
        like_percentage = round((likes_count / total_ratings) * 100)
    else:
        like_percentage = 0

    # Возвращаем HTML фрагмент
    return render(request, 'partials/rating_block.html', {
        'manga': manga,
        'chapter': chapter,
        'like_percentage': like_percentage,
        'user_rating': user_rating
    })