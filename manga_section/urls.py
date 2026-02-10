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
    path('page/<int:page_id>/comments/', views.find_comments, name='find-comments'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:comment_id>/delete/', views.remove_comment, name='remove-comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)