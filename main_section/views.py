import random
from decimal import Decimal

from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import csrf_token
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import logout
from django.utils.regex_helper import next_char
from django.views.decorators.http import require_http_methods

from main_section.forms import RegisterForm
from manga_section.models import Chapter, Volume, Manga, ChapterImage
from post_section.forms import FAQform
from post_section.models import Post, MessageFAQ

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json

from django.middleware.csrf import get_token

from django.contrib.auth.views import LoginView
from .forms import LoginFormWithCaptcha
from .models import ChapterLike, ChapterView


class CustomLoginView(LoginView):
    form_class = LoginFormWithCaptcha
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_mobile'] = getattr(self.request, 'is_mobile', False)
        return context

def index(request):
    # return render(request, 'top_panel.html')
    return redirect('home-page')


def register_view(request):
    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_from_form = request.POST.get('next')
            if next_from_form and next_from_form.startswith('/'):
                if next_from_form.strip() != '/':
                    return redirect(next_from_form)
            return redirect('home-page')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form, 'next': next_url})

@require_http_methods(["GET"])
def custom_logout(request):
    logout(request)
    return redirect('login')


def main_page(request):
    random_manga = None
    random_post = None
    random_volume = None
    last_week = timezone.now() - timezone.timedelta(days=7)
    recent_chapters = Chapter.objects.filter(
        add_date__gte=last_week
    ).select_related(
        'volume__manga'
    ).prefetch_related(
        Prefetch('volume__manga__volumes',
                 queryset=Volume.objects.order_by('-vol_number'),
                 to_attr='latest_volumes')
    ).order_by('-add_date')

    if recent_chapters.exists():
        manga_dict = {}
        for chapter in recent_chapters:
            manga = chapter.volume.manga
            if manga.id not in manga_dict:
                latest_volume = manga.volumes.order_by('-vol_number').first()
                cover = latest_volume.vol_cover if latest_volume else None

                manga_dict[manga.id] = {
                    'manga': manga,
                    'cover': cover,
                    'chapters': []
                }
            manga_dict[manga.id]['chapters'].append(chapter)
    else:
        manga_dict = {}
        manga = Manga.objects.all()
        random_manga = random.choice(list(manga))
        volumes = random_manga.volumes.order_by('vol_number')
        random_volume = random.choice(volumes)

    # recent_posts = Post.objects.filter(add_date__gte=last_week, visibility=True).order_by('-add_date')
    recent_posts = Post.objects.order_by('-add_date').first()

    # if not recent_posts.exists():
    #     recent_posts = {}
    #     posts = Post.objects.exclude(visibility=0)
    #     random_post = random.choice(list(posts))

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    context = {
        'recent_manga': list(manga_dict.values()),
        'recent_post': recent_posts,
        'manga': random_manga,
        'volume': random_volume,
        'post': random_post,
        'messages_cnt': message_cnt
    }
    return render(request, 'main_page.html', context)

# @login_required(login_url='/login/')
def info_page(request):
    post = get_object_or_404(Post, post_slug='info')

    if request.method == 'POST':
        form = FAQform(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()
            return HttpResponseRedirect('/info/')
    else:
        form = FAQform()

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    context = {
        'post': post,
        'form': form,
        'messages_cnt': message_cnt
    }

    return render(request, 'post_page.html', context)


@login_required
def get_theme_preference(request):
    """Получить сохранённую тему пользователя"""
    try:
        theme = request.user.profile.theme
        return JsonResponse({
            'status': 'success',
            'theme': theme,
            'username': request.user.username
        })
    except Exception as e:
        # Если профиль не существует, создаём его
        from .models import Profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        return JsonResponse({
            'status': 'success',
            'theme': profile.theme,
            'username': request.user.username
        })


@csrf_exempt
@login_required
def save_theme_preference(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            theme = data.get('theme')

            if theme in ['auto', 'light', 'dark']:
                # Сохраняем в профиль пользователя
                request.user.profile.theme = theme
                request.user.profile.save()

                # Также сохраняем в localStorage на клиенте
                return JsonResponse({
                    'status': 'success',
                    'message': 'Тема сохранена',
                    'theme': theme
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Неверная тема'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешен'})

def message_count(request):
    messages_cnt = MessageFAQ.objects.filter(is_read=False).count()
    return messages_cnt

def messages_page(request):
    if request.user.username == 'yurden':
        messages = MessageFAQ.objects.all()

        if request.user.username == 'yurden':
            message_cnt = message_count(request)
        else:
            message_cnt = 0

        context = {
            'messages': messages,
            'messages_cnt': message_cnt
        }

        return render(request, 'message_catalog.html', context)
    else:
        return redirect('home-page')

def read_message(request, message_id):
    message = get_object_or_404(MessageFAQ, pk=message_id)

    message.is_read = not message.is_read
    message.save()

    unread_count = MessageFAQ.objects.filter(is_read=False).count()

    csrf_token = get_token(request)

    button_html = render_to_string('partials/message_read_block.html', {'message': message, 'csrf_token': csrf_token})

    response = HttpResponse()
    response.write(f'<div id="unread-counter" hx-swap-oob="true"><p>{unread_count}</p></div>')
    response.write(button_html)

    return response

    # return render(request, 'partials/message_read_block.html', {'message': message})

def close_tutorial(request):
    if request.method == 'POST':
        user = request.user

        user.profile.viewed_tutorial = True
        user.profile.save()

        return HttpResponse('<div id="tutorial_block"></div>')

def single_close_tutorial(request):
    if request.method == 'POST':
        user = request.user

        user.profile.viewed_single = True
        user.profile.save()

        return HttpResponse('<div id="tutorial_block"></div>')

def double_close_tutorial(request):
    if request.method == 'POST':
        user = request.user

        user.profile.viewed_double = True
        user.profile.save()

        return HttpResponse('<div id="tutorial_block"></div>')