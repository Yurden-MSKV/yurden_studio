from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


def index(request):
    """Главная страница - список последних 5 опросов"""
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    context = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'poll_section/index.html', context)


def detail(request, question_id):
    """Страница детального просмотра вопроса с формой голосования"""
    question = get_object_or_404(Question, pk=question_id)

    context = {
        'question': question,
    }

    return render(request, 'poll_section/detail.html', context)


def vote(request, question_id):
    """Обработка отправленной формы голосования"""
    question = get_object_or_404(Question, pk=question_id)

    try:
        # Получаем выбранный вариант ответа из POST-данных
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Если вариант не был выбран, показываем форму снова с ошибкой

        context = {
            'question': question,
            'error_message': "Пожалуйста, выберите вариант ответа.",
        }

        return render(request, 'poll_section/detail.html', context)

    else:
        # Увеличиваем счетчик голосов и сохраняем
        selected_choice.votes += 1
        selected_choice.save()

        # Перенаправляем на страницу результатов
        return HttpResponseRedirect(reverse('poll_section:results', args=(question.id,)))


def results(request, question_id):
    """Страница с результатами голосования"""
    question = get_object_or_404(Question, pk=question_id)

    context = {
        'question': question,
    }

    return render(request, 'poll_section/results.html', context)