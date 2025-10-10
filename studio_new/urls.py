from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from main_section import views as main_section_views
from main_section.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_section_views.index),
    path('home/', main_section_views.main_page, name='home-page'),
    path('manga/', include('manga_section.urls')),
    path('post/', include('post_section.urls')),
    path('polls/', include('poll_section.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('register/', main_section_views.register_view, name='register'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', main_section_views.custom_logout, name='logout'),
    path('info/', main_section_views.info_page, name='info'),
path('api/save-theme/', main_section_views.save_theme_preference, name='save_theme'),
path('api/get-theme/', main_section_views.get_theme_preference, name='get_theme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)