from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from main_section.views import message_count
from post_section.forms import PostCommentForm
from post_section.models import Post, PostComment


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
    post = get_object_or_404(Post.objects.prefetch_related('tags'), post_slug=post_slug)
    tags = post.tags.all()

    if request.user.username == 'yurden':
        message_cnt = message_count(request)
    else:
        message_cnt = 0

    if not request.user.is_superuser:
        viewed_key = f'viewed_post_{post.id}'
        if not request.COOKIES.get(viewed_key):
            post.view_count += 1
            post.save()

            response = render(request, 'post_page.html', {'post': post})
            response.set_cookie(viewed_key, 'true', max_age=300)
            return response

    return render(request, 'post/new_post_page.html', {
        'post': post,
        'tags': tags,
        'messages_cnt': message_cnt,
    })


def find_post_comments(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            print(comment)
            form = PostCommentForm()
            comments = post.comments.all().order_by('created_at')
        else:
            print(f"Form errors: {form.errors}")

        context = {
            'post': post,
            'post_id': post.id,
            'form': form,
            'comments': comments
        }

        return render(request, 'post/comments/post_comments_block.html', context)

    else:
        form = PostCommentForm()

        context = {
            'post': post,
            'post_id': post.id,
            'form': form,
            'comments': comments
        }

        return render(request, 'post/comments/post_comments_block.html', context)

def comment_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(PostComment, id=comment_id)

    if request.method == "POST":
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent_comment = parent_comment
            comment.save()
            print(comment)
            form = PostCommentForm()
            comments = post.comments.all().order_by('created_at')

            context = {
                'post': post,
                'post_id': post.id,
                'form': form,
                'comments': comments,
            }

            return render(request, 'post/comments/post_comments_block.html', context)

        else:
            print(f"Form errors: {form.errors}")
            return None

    else:
        form = PostCommentForm()
        context = {
            'post': post,
            'form': form,
            'post_id': post.id,
            'comment_id': parent_comment.id
        }
        return render(request, 'post/comments/reply_block.html', context)


def show_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(PostComment, id=comment_id)

    context = {
        'comment': parent_comment
    }

    return render(request, 'post/comments/parent_comment.html', context)