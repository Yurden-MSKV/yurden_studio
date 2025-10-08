// static/post_section/js/poll.js

let userVoted = window.userVoted || false;
let userChoiceId = window.userChoiceId || null;

// Функция голосования
function vote(choiceId) {
    console.log('Голосую за:', choiceId);

    // Показываем загрузку
    const voteButtons = document.querySelectorAll('.vote-btn');
    voteButtons.forEach(btn => {
        btn.disabled = true;
        if (btn.getAttribute('data-choice-id') === choiceId.toString()) {
            btn.textContent = 'Голосую...';
        }
    });

    // Отправляем AJAX запрос
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            action: 'vote',
            choice_id: choiceId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Ответ сервера:', data);
        if (data.success) {
            // Обновляем интерфейс БЕЗ перезагрузки
            userVoted = true;
            userChoiceId = choiceId;
            // Просто переключаем видимость блоков
            switchToResults();
            resetButtons(); // Сбрасываем состояние кнопок голосования
        } else {
            alert('Ошибка: ' + data.error);
            resetButtons();
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при голосовании');
        resetButtons();
    });
}

// Функция отмены голоса
function cancelVote() {
    console.log('Отменяю голос');

    // Показываем загрузку
    const cancelBtn = document.querySelector('.cancel-btn');
    if (cancelBtn) {
        cancelBtn.textContent = 'Отменяю...';
        cancelBtn.disabled = true;
    }

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            action: 'cancel'
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Ответ сервера:', data);
        if (data.success) {
            // Обновляем интерфейс БЕЗ перезагрузки
            userVoted = false;
            userChoiceId = null;
            // Переключаем обратно на кнопки голосования
            switchToVoteButtons();
            resetCancelButton(); // Сбрасываем состояние кнопки отмены
        } else {
            alert('Ошибка: ' + data.error);
            resetCancelButton();
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при отмене голоса');
        resetCancelButton();
    });
}

// Переключаем на блок с результатами
function switchToResults() {
    const resultsDiv = document.getElementById('results');
    const voteButtonsDiv = document.getElementById('vote-buttons');

    voteButtonsDiv.style.display = 'none';
    resultsDiv.style.display = 'block';
    console.log('Переключили на результаты');

    // Сбрасываем состояние кнопки отмены на случай, если она была в состоянии загрузки
    resetCancelButton();
}

// Переключаем на блок с кнопками голосования
function switchToVoteButtons() {
    const resultsDiv = document.getElementById('results');
    const voteButtonsDiv = document.getElementById('vote-buttons');

    voteButtonsDiv.style.display = 'flex';
    resultsDiv.style.display = 'none';
    resetButtons();
    console.log('Переключили на кнопки голосования');
}

// Вспомогательные функции
function resetButtons() {
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.disabled = false;
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.textContent = originalText;
        }
    });
}

function resetCancelButton() {
    const cancelBtn = document.querySelector('.cancel-btn');
    if (cancelBtn) {
        cancelBtn.textContent = '✖ Отменить мой голос';
        cancelBtn.disabled = false;
    }
}

// Функция для CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Poll JS загружен', { userVoted, userChoiceId });

    // Сохраняем оригинальные тексты кнопок
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.setAttribute('data-original-text', button.textContent);

        // Назначаем обработчики клика
        button.addEventListener('click', function() {
            if (!this.disabled) {
                const choiceId = this.getAttribute('data-choice-id');
                console.log('Клик по кнопке:', choiceId);
                vote(parseInt(choiceId));
            }
        });
    });

    // Убедимся, что кнопка отмены в правильном состоянии при загрузке
    resetCancelButton();
});