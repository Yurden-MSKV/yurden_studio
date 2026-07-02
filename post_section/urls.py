from django.urls import path
from post_section import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_catalog, name='post-catalog'),
    path('<slug:post_slug>/', views.post_page, name='post-page'),
    path('<int:id>/comments/', views.find_post_comments, name='find_post_comments'),
    path('<int:post_id>/new-comment/', views.load_new_form, name='post-load-new-form'),
    path('<int:post_id>/comments/<int:comment_id>/reply/', views.comment_reply, name='reply'),
    path('<int:post_id>/comments/<int:comment_id>/', views.show_reply, name='show_reply'),
    path('<int:post_id>/comments/<int:comment_id>/edit/', views.edit_post_comment, name='edit-post-comment'),
    # path('<int:post_id>/comments/<int:comment_id>/delete/', views.delete_post_comment, name='delete-post-comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)