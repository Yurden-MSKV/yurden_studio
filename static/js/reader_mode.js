const READER_MODE = {
    LEFT_TO_RIGHT: 'left_to_right',
    RIGHT_TO_LEFT: 'right_to_left'
};

let currentReaderMode = 'left_to_right';


function switchModeButton(nextMode) {
    document.querySelectorAll('.reader-icon').forEach(icon => {
        icon.classList.remove('show');
    })
    const nextButton = document.querySelectorAll(`.${nextMode}_icon`);
    if (nextButton) {
        nextButton.forEach(button => {
            button.classList.add('show')
        })
    }
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

async function loadUserMode() {
    const modeResponse = await fetch('/api/get-reader-mode/');
    if (modeResponse.ok) {
        const modeResult = await modeResponse.json();
        if (modeResult.status === 'success' && modeResult.mode) {
            return modeResult.mode;
        }
    }
}

async function saveModeToServer(nextMode) {
    await fetch('/api/save-reader-mode/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({mode: nextMode})
    });
}

async function switchReaderMode() {
    let nextMode;
    if (currentReaderMode === READER_MODE.LEFT_TO_RIGHT) {
        nextMode = READER_MODE.RIGHT_TO_LEFT;
    } else {
        nextMode = READER_MODE.LEFT_TO_RIGHT;
    }

    currentReaderMode = nextMode;
    switchModeButton(nextMode);
    localStorage.setItem('readerMode', nextMode);
    await saveModeToServer(nextMode);
}

async function setupCurrentMode() {
    let nextMode = await loadUserMode();
    if (nextMode) {
        currentReaderMode = nextMode;
        switchModeButton(nextMode);
    }
}

    function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

document.addEventListener('DOMContentLoaded', function () {
    setupCurrentMode();
    const readerButton = document.getElementById('readerToggle');
    const readerButtonMobile = document.getElementById('readerToggleMobile');
    const debouncedSwitchReaderMode = debounce(switchReaderMode, 150);
    if (readerButton || readerButtonMobile) {
        readerButton.addEventListener('click', debouncedSwitchReaderMode)
        readerButtonMobile.addEventListener('click', debouncedSwitchReaderMode)
    }
})