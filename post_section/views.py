from django.shortcuts import render, get_object_or_404

from main_section.views import message_count
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

    if not request.user.is_superuser:
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

    # Обычный GET запрос - передаем результаты в шаблон
    return render(request, 'post_page.html', {
        'post': post,
        'messages_cnt': message_cnt,
    })