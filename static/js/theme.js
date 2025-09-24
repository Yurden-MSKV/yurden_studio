// Состояния темы
const THEME_STATES = {
    AUTO: 'auto',
    LIGHT: 'light',
    DARK: 'dark'
};

// Текущее состояние темы
let currentThemeState = THEME_STATES.AUTO;

// Функция проверки аутентификации пользователя
function isUserAuthenticated() {
    return document.body.querySelector('.profile_button_block') !== null ||
           document.body.querySelector('.profile_container') !== null ||
           document.getElementById('userMenu') !== null;
}

// Функция определения темы по времени
function getThemeByTime() {
    const hour = new Date().getHours();
    return (hour >= 19 || hour < 7) ? THEME_STATES.DARK : THEME_STATES.LIGHT;
}

// Функция применения темы к body
function applyThemeToBody(theme) {
    document.body.classList.remove('light-theme', 'dark-theme');

    if (theme === THEME_STATES.LIGHT) {
        document.body.classList.add('light-theme');
    } else if (theme === THEME_STATES.DARK) {
        document.body.classList.add('dark-theme');
    }
}

// Функция переключения видимости иконок
function switchIconVisibility(nextState) {
    document.querySelectorAll('.theme-icon').forEach(icon => {
        icon.classList.remove('show');
    });

    const nextIcon = document.querySelector(`.${nextState}-icon`);
    if (nextIcon) {
        nextIcon.classList.add('show');
    }
}

// Функция получения CSRF токена
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Функция загрузки темы пользователя
async function loadUserTheme() {
    try {
        const response = await fetch('/api/get-theme/');
        if (response.ok) {
            const result = await response.json();
            if (result.status === 'success' && result.theme) {
                return result.theme;
            }
        } else if (response.status === 403) {
            return null;
        }
    } catch (error) {
        console.error('Ошибка загрузки темы:', error);
    }
    return null;
}

// Функция сохранения темы на сервере
async function saveThemeToServer(theme) {
    if (!isUserAuthenticated()) {
        return;
    }

    try {
        const response = await fetch('/api/save-theme/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ theme: theme })
        });

        if (response.ok) {
            const result = await response.json();
            if (result.status === 'success') {
                console.log('Тема сохранена на сервере:', theme);
            }
        }
    } catch (error) {
        console.error('Ошибка при сохранении темы на сервере:', error);
    }
}

// Функция переключения темы
async function switchTheme() {
    let nextState;
    switch (currentThemeState) {
        case THEME_STATES.AUTO:
            nextState = THEME_STATES.LIGHT;
            break;
        case THEME_STATES.LIGHT:
            nextState = THEME_STATES.DARK;
            break;
        case THEME_STATES.DARK:
            nextState = THEME_STATES.AUTO;
            break;
        default:
            nextState = THEME_STATES.AUTO;
    }

    currentThemeState = nextState;
    switchIconVisibility(nextState);

    if (nextState === THEME_STATES.AUTO) {
        applyThemeToBody(getThemeByTime());
    } else {
        applyThemeToBody(nextState);
    }

    localStorage.setItem('themeState', nextState);
    await saveThemeToServer(nextState);
}

// Полная инициализация темы после загрузки страницы
async function setupThemeAfterLoad() {
    const userAuthenticated = isUserAuthenticated();
    let userTheme = null;

    if (userAuthenticated) {
        try {
            userTheme = await loadUserTheme();
        } catch (error) {
            // Игнорируем ошибки загрузки
        }
    }

    if (userTheme && userTheme !== 'default') {
        currentThemeState = userTheme;
    } else {
        const savedState = localStorage.getItem('themeState');
        if (savedState && Object.values(THEME_STATES).includes(savedState)) {
            currentThemeState = savedState;
        }
    }

    // Применяем тему (inline JS уже применил базовую, это для точности)
    if (currentThemeState === THEME_STATES.AUTO) {
        applyThemeToBody(getThemeByTime());
    } else {
        applyThemeToBody(currentThemeState);
    }

    switchIconVisibility(currentThemeState);
}

// Автоматическое обновление темы для режима AUTO
function startAutoThemeUpdate() {
    setInterval(() => {
        if (currentThemeState === THEME_STATES.AUTO) {
            applyThemeToBody(getThemeByTime());
        }
    }, 60 * 60 * 1000);
}

// Проверка граничного времени
function startMinuteCheck() {
    setInterval(() => {
        if (currentThemeState === THEME_STATES.AUTO) {
            const currentHour = new Date().getHours();
            if (currentHour === 7 || currentHour === 19) {
                applyThemeToBody(getThemeByTime());
            }
        }
    }, 60 * 1000);
}

// Инициализация после полной загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    setupThemeAfterLoad();

    const themeButton = document.getElementById('themeToggle');
    if (themeButton) {
        themeButton.addEventListener('click', switchTheme);
    }

    startAutoThemeUpdate();
    startMinuteCheck();
});