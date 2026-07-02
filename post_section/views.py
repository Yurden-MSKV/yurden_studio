from django.contrib.auth.decorators import login_required
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

    if tags:
        print('1 вариант')
        tags_flag = True
    else:
        print('2 вариант')
        tags_flag = False



    return render(request, 'post/new_post_page.html', {
        'post': post,
        'tags': tags,
        'tags_flag': tags_flag
    })


@login_required
def load_new_form(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            print(comment)
            comments = [comment]
            context = {
                'post': post,
                'comments': comments
            }
            return render(request, 'post/comments/post_comments_list.html', context)

    else:
        form = PostCommentForm()
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'post/comments/new_comment_form.html', context)


def find_post_comments(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('created_at')

    context = {
        'post': post,
        'comments': comments,
    }

    return render(request, 'post/comments/post_comments_list.html', context)


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

            comments = [comment]

            context = {
                'post': post,
                'comments': comments,
            }

            return render(request, 'post/comments/post_comments_list.html', context)

    else:
        form = PostCommentForm()
        context = {
            'post': post,
            'form': form,
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


@login_required
def edit_post_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(PostComment, pk=comment_id)
    if comment.author == request.user:
        if request.method == 'POST':
            form = PostCommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.save()
                comments = [comment]
                return render(request, 'post/comments/post_comments_list.html', {'comments': comments, 'post': post})
        else:
            form = PostCommentForm(instance=comment)
            return render(request, 'post/comments/post_edit_comment.html', {'form': form, 'post': post, 'comment': comment})

# @login_required
# def delete_post_comment(request, post_id, comment_id):
#     ...
