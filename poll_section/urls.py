from django.urls import path
from . import views

# Пространство имен для организации URL
# app_name = 'poll_section'

urlpatterns = [
    # # Главная страница опросов - список всех вопросов
    # path('', views.index, name='index'),
    #
    # # Страница детального просмотра вопроса с формой для голосования
    # path('<int:question_id>/', views.detail, name='detail'),
    #
    # # Обработка отправки формы голосования
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    #
    # # Страница с результатами голосования
    # path('<int:question_id>/results/', views.results, name='results'),
]