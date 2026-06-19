from django.urls import path
from manga_section import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.catalog_page, name='catalog-page'),
    path('<slug:slug>/', views.manga_page, name='manga-page'),
    # path('<slug:manga_slug>/chapter/<str:ch_number>/', views.chapter_page, name='chapter-page'),
    path('<slug:manga_slug>/chapter/<str:ch_number>/', views.new_reader, name='chapter-page'),
    path('<slug:manga_slug>/chapter/<str:ch_number>/rate/', views.rate_chapter, name='rate-chapter'),
    path('page/<int:page_id>/comments/', views.load_chapter_comments, name='load-comments'),
    path('page/<int:page_id>/new-comment/', views.load_new_comment_form, name='load-new-form'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:comment_id>/delete/', views.remove_comment, name='remove-comment'),
    path('comment/<int:comment_id>/reply/', views.comment_reply, name='comment_reply'),
    path('comment/<int:comment_id>/', views.show_reply, name='show-comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)