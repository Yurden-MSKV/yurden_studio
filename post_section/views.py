import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from main_section.views import message_count
from poll_section.models import Choice, Vote
from post_section.models import Post

def post_catalog(request):
    post_list = Post.objects.filter(visibility=True).order_by('-add_date')

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    context = {
        'post_list': post_list,
        'messages_cnt': message_cnt,
    }

    return render(request, "post_catalog_page.html", context)

def post_page(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    poll = None
    choices = None
    user_vote = None
    results_data = None

    # Проверяем, есть ли куки, что пользователь уже просматривал этот пост
    viewed_key = f'viewed_post_{post.id}'
    if not request.COOKIES.get(viewed_key):
        # Увеличиваем счетчик просмотров
        post.view_count += 1
        post.save()

        # Устанавливаем куки на 5 минут (300 секунд)
        response = render(request, 'post_page.html', {'post': post})
        response.set_cookie(viewed_key, 'true', max_age=300)
        return response

    if post.polls.exists():
        poll = post.polls.first()
        choices = poll.choices.all()

        # Получаем результаты ВСЕГДА (и для GET и для POST)
        results_data = get_poll_results(poll)

        # Проверяем голос пользователя
        if request.user.is_authenticated:
            user_vote = Vote.objects.filter(choice__poll=poll, user=request.user).first()

    # ЕСЛИ ЭТО AJAX ЗАПРОС
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Для голосования необходимо авторизоваться'})

        data = json.loads(request.body)
        action = data.get('action')
        choice_id = data.get('choice_id')

        try:
            if action == 'vote':
                # Проверяем, не голосовал ли уже
                existing_vote = Vote.objects.filter(choice__poll=poll, user=request.user).first()
                if existing_vote:
                    return JsonResponse({'success': False, 'error': 'Вы уже проголосовали'})

                # Сохраняем голос
                choice = Choice.objects.get(id=choice_id)
                Vote.objects.create(choice=choice, user=request.user)

            elif action == 'cancel':
                # Удаляем голос
                Vote.objects.filter(choice__poll=poll, user=request.user).delete()

            # ОБНОВЛЯЕМ результаты после голосования/отмены
            results_data = get_poll_results(poll)

            return JsonResponse({
                'success': True,
                'results': results_data['results'],
                'total_votes': results_data['total_votes'],
                'user_voted': action == 'vote'
            })

        except Choice.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Вариант не найден'})

    # Обычный GET запрос - передаем результаты в шаблон
    return render(request, 'post_page.html', {
        'post': post,
        'poll': poll,
        'choices': choices,
        'user_vote': user_vote,
        'results_data': results_data,  # Передаем результаты в шаблон
        'messages_cnt': message_cnt,
    })

def get_poll_results(poll):
    if not poll:
        return {'results': [], 'total_votes': 0}

    choices = poll.choices.all()
    results = []
    total_votes = Vote.objects.filter(choice__poll=poll).count()

    for choice in choices:
        vote_count = Vote.objects.filter(choice=choice).count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        results.append({
            'choice_text': choice.choice_text,
            'vote_count': vote_count,
            'percentage': round(percentage, 1),
            'choice_id': choice.id
        })

    return {
        'results': results,
        'total_votes': total_votes
    }