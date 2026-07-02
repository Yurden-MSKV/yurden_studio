from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main_section import views as main_section_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('close_tutorial/', main_section_views.close_tutorial, name='close-tutorial'),
    path('single_close_tutorial/', main_section_views.single_close_tutorial, name='single-close-tutorial'),
    path('double_close_tutorial/', main_section_views.double_close_tutorial, name='double-close-tutorial'),
    path('', main_section_views.index),
    # path('home/', main_section_views.main_page, name='home-page'),
    path('home/', main_section_views.new_home_page, name='new-home'),
    # path('feed/', main_section_views.new_home_page, name='feed'),
    path('manga/', include('manga_section.urls')),
    path('post/', include('post_section.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('register/', main_section_views.register_view, name='register'),
    # path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login/', main_section_views.CustomLoginView.as_view(), name='login'),
    path('logout/', main_section_views.custom_logout, name='logout'),
    path('info/', main_section_views.info_page, name='info'),
    path('messages/', main_section_views.messages_page, name='messages'),
    path('messages/read/<int:message_id>/', main_section_views.read_message, name='read-message'),
    path('api/save-theme/', main_section_views.save_theme_preference, name='save_theme'),
    path('api/get-theme/', main_section_views.get_theme_preference, name='get_theme'),
    path('api/save-reader-mode/', main_section_views.save_reader_mode, name='save_mode'),
    path('api/get-reader-mode/', main_section_views.get_reader_mode, name='get_mode'),
    path('new-top/', main_section_views.top_panel_test, name='top-panel-test'),
    path('reset-reader/', main_section_views.reset_reader, name='reset_reader'),
    path('reset-reader-mobile/', main_section_views.reset_reader_mobile, name='reset_reader_mobile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]