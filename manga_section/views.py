from django.http import Http404, JsonResponse, HttpResponse
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from main_section.views import message_count
from manga_section.forms import CommentForm
from manga_section.models import Manga, Chapter, ChapterImage, Comment
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

    user_rates_list = list(
        ChapterLike.objects.filter(user=request.user, manga=manga).values_list('chapter_id', flat=True))
    user_rates = user_rates_list

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
        'user_rates': user_rates,
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
        ch_number=chapter_number_decimal
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

def new_reader(request, manga_slug, ch_number):

    manga = get_object_or_404(Manga, manga_slug=manga_slug)
    chapter_number_decimal = Decimal(ch_number)
    chapter = get_object_or_404(Chapter.objects.filter(volume__manga=manga), ch_number=chapter_number_decimal)

    if request.user.is_superuser:
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
        ch_number__lt=chapter_number_decimal
    ).order_by('-ch_number').first()
    next_chapter = Chapter.objects.filter(
        volume__manga=manga,
        ch_number__gt=chapter_number_decimal
    ).order_by('ch_number').first()

    pages = ChapterImage.objects.filter(chapter=chapter).order_by('page_number')

    single_page_mode = []
    i = 0
    while i < len(pages):
        single_page_mode.append(pages[i])
        i += 1

    double_page_mode = []
    i = 0
    while i < len(pages):
        current_page = pages[i]

        # Если текущая страница - разворот
        if current_page.is_double_page or current_page.page_number == 1:
            double_page_mode.append([current_page])  # Добавляем как одиночный элемент
            i += 1
            continue

        # Если следующая страница существует и не является разворотом
        if i + 1 < len(pages) and not pages[i + 1].is_double_page:
            double_page_mode.append([current_page, pages[i + 1]])
            i += 2
        else:
            # Если следующая страница - разворот или последняя страница
            double_page_mode.append([current_page])
            i += 1

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
        'single_page_mode': single_page_mode,
        'double_page_mode': double_page_mode,
        'like_percentage': like_percentage,
        'user_rating': user_rating,
        'prev_chapter': prev_chapter.get_chapter_display if prev_chapter else None,
        'next_chapter': next_chapter.get_chapter_display if next_chapter else None,
    }

    return render(request, 'new_chapter_page.html', context)


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

    # Определяем, из какого блока пришел запрос
    source_block = request.POST.get('source_block', 'single')

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
            manga=manga,
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

    context = {
        'manga': manga,
        'chapter': chapter,
        'like_percentage': like_percentage,
        'user_rating': user_rating
    }

    if request.htmx:
        # Рендерим оба блока
        single_html = render_to_string('partials/single_rating_block.html', context)
        double_html = render_to_string('partials/double_rating_block.html', context)

        # Возвращаем оба блока с использованием hx-swap-oob
        response_html = f"""
        <div hx-swap-oob="outerHTML:.single_rating">{single_html}</div>
        <div hx-swap-oob="outerHTML:.double_rating">{double_html}</div>
        """

        # Для совместимости с исходным запросом, также возвращаем основной контент
        if source_block == 'single':
            response_html = single_html + f"\n<div hx-swap-oob=\"outerHTML:.double_rating\">{double_html}</div>"
        else:
            response_html = double_html + f"\n<div hx-swap-oob=\"outerHTML:.single_rating\">{single_html}</div>"

        return HttpResponse(response_html)

    # Для не-HTML запросов (на всякий случай)
    return JsonResponse({
        'like_percentage': like_percentage,
        'user_rating': user_rating
    })

def find_comments(request, page_id):
    page = get_object_or_404(ChapterImage, pk=page_id)
    comments = page.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.manga = page.chapter.volume.manga
            comment.chapter = page.chapter
            comment.page = page
            comment.save()
            form = CommentForm()

            comments = page.comments.all().order_by('-created_at')

            return render(request, 'partials/comments_block.html', {
                'page': page,
                'page_id': page_id,
                'comments': comments,
                'form': form,
            })

    else:
        form = CommentForm()

    context = {
        'page': page,
        'page_id': page_id,
        'comments': comments,
        'form': form,
    }

    return render(request, 'partials/comments_block.html', context)

def remove_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    page = comment.page
    if comment.author == request.user:
        comment.delete()
        if page.comments.count() > 0:
            return HttpResponse("<div style='display: none'></div>")
        else:
            return HttpResponse("<div class='no_comments'><p>У этой страницы нет комментариев. Напишешь первый?</p></div>")
    else:
        return HttpResponse("<p style='color: red'>Это не твой комментарий.</p>")

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user or request.user.username == 'yurden':
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.save()
                page = comment.page
                page_id = page.id
                comments = page.comments.all().order_by('-created_at')
                form = CommentForm()
                return render(request, 'partials/comments_block.html', {
                    'page': page,
                    'page_id': page_id,
                    'comments': comments,
                    'form': form,
                })
        else:
            form = CommentForm(instance=comment)
            return render(request, 'partials/edit_comment.html',{'form': form, 'comment': comment})
    else:
        return HttpResponse("<p style='color: red'>Это не твой комментарий.</p>")