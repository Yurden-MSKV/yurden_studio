// static/post_section/js/poll.js

class PollManager {
    constructor() {
        this.userVoted = window.pollData.userVoted;
        this.userChoiceId = window.pollData.userChoiceId;
        this.init();
    }

    init() {
        console.log('Poll initialized');
        this.bindEvents();
        this.applyWidthsFromDataAttributes(); // Применяем ширины при загрузке
    }

    bindEvents() {
        document.querySelectorAll('.vote-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                if (!button.disabled) {
                    this.vote(parseInt(button.dataset.choiceId));
                }
            });
        });
    }

    // НОВАЯ ФУНКЦИЯ: Применяем ширины из data-атрибутов
    applyWidthsFromDataAttributes() {
        document.querySelectorAll('.progress-fill[data-width]').forEach(bar => {
            const width = bar.getAttribute('data-width');
            if (width) {
                // Используем CSS переменную как fallback
                bar.style.setProperty('--progress-width', width + '%');
                // И прямое назначение
                bar.style.width = width + '%';

                console.log('Applied width:', width + '%', 'to element:', bar);
            }
        });
    }

    async vote(choiceId) {
        console.log('Voting for:', choiceId);
        this.setButtonsState(true, choiceId);

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    action: 'vote',
                    choice_id: choiceId
                })
            });

            if (!response.ok) throw new Error('Network error');
            const data = await response.json();

            if (data.success) {
                this.userVoted = true;
                this.userChoiceId = choiceId;
                this.showResults(data.results, data.total_votes);
            } else {
                alert('Ошибка: ' + data.error);
                this.setButtonsState(false);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ошибка при голосовании');
            this.setButtonsState(false);
        }
    }

    async cancelVote() {
        console.log('Canceling vote');
        const cancelBtn = document.querySelector('.cancel-vote-btn');
        if (cancelBtn) {
            cancelBtn.textContent = 'Отменяю...';
            cancelBtn.disabled = true;
        }

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    action: 'cancel'
                })
            });

            if (!response.ok) throw new Error('Network error');
            const data = await response.json();

            if (data.success) {
                this.userVoted = false;
                this.userChoiceId = null;
                this.showVoteButtons(data.results, data.total_votes);
            } else {
                alert('Ошибка: ' + data.error);
                this.resetCancelButton();
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ошибка при отмене голоса');
            this.resetCancelButton();
        }
    }

    showResults(results, totalVotes) {
        const voteSection = document.getElementById('vote-section');
        const resultsSection = document.getElementById('results-section');

        let resultsHTML = '<div class="results-container">';

        results.forEach(result => {
            const isUserChoice = this.userChoiceId && result.choice_id == this.userChoiceId;
            const percentage = totalVotes > 0 ? new Intl.NumberFormat('ru-RU', {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
            }).format(parseFloat(result.percentage)) : '0';

            resultsHTML += `
                <div class="result-row">
                    <div class="result-info">
                        <span class="choice-text"><p>${result.choice_text}</p></span>
                        <span class="vote-count"><p>${result.vote_count} голосов</p></span>
                    </div>
                    <div class="result_graph">
                        <div class="result-visual">
                            <div class="progress-bar">
                                <div class="progress-fill ${isUserChoice ? 'user-choice' : ''}" 
                                     data-width="${percentage.replace(',', '.')}">
                                </div>
                            </div>
                        </div>
                        <span class="progress-text"><p>${percentage}%</p></span>
                        ${isUserChoice ? '<div class="user-badge"><p>[твой выбор]</p></div>' : ''}
                    </div>
                </div>
            `;
        });

        resultsHTML += `
            <button type="button" class="cancel-vote-btn" onclick="pollManager.cancelVote()">
                ✖ Отменить мой голос
            </button>
        </div>`;

        resultsSection.innerHTML = resultsHTML;
        voteSection.style.display = 'none';
        resultsSection.style.display = 'block';
        this.setButtonsState(false);

        // Применяем ширины сразу
        setTimeout(() => this.applyWidthsFromDataAttributes(), 10);
    }

    showVoteButtons(results, totalVotes) {
        const voteSection = document.getElementById('vote-section');
        const resultsSection = document.getElementById('results-section');

        if (totalVotes > 0) {
            let resultsHTML = '<div class="results-container">';

            results.forEach(result => {
                const percentage = totalVotes > 0 ? new Intl.NumberFormat('ru-RU', {
                    minimumFractionDigits: 1,
                    maximumFractionDigits: 1
                }).format(parseFloat(result.percentage)) : '0';

                resultsHTML += `
                    <div class="result-row">
                        <div class="result-info">
                            <span class="choice-text"><p>${result.choice_text}</p></span>
                            <span class="vote-count"><p>${result.vote_count} голосов</p></span>
                        </div>
                        <div class="result_graph">
                            <div class="result-visual">
                                <div class="progress-bar">
                                    <div class="progress-fill" data-width="${percentage.replace(',', '.')}">
                                    </div>
                                </div>
                            </div>
                            <span class="progress-text"><p>${percentage}%</p></span>
                        </div>
                    </div>
                `;
            });

            resultsHTML += '</div>';
            resultsSection.innerHTML = resultsHTML;
        } else {
            resultsSection.innerHTML = '<p>Пока нет голосов. Будьте первым!</p>';
        }

        voteSection.style.display = 'block';
        resultsSection.style.display = 'none';
        this.resetCancelButton();

        // Применяем ширины сразу
        setTimeout(() => this.applyWidthsFromDataAttributes(), 10);
    }

    setButtonsState(disabled, loadingText = null, activeChoiceId = null) {
        document.querySelectorAll('.vote-btn').forEach(button => {
            button.disabled = disabled;
            if (loadingText && parseInt(button.dataset.choiceId) === activeChoiceId) {
                button.textContent = loadingText;
            } else if (!disabled) {
                button.textContent = button.dataset.originalText || button.textContent;
            }
        });
    }

    resetCancelButton() {
        const cancelBtn = document.querySelector('.cancel-vote-btn');
        if (cancelBtn) {
            cancelBtn.textContent = '✖ Отменить мой голос';
            cancelBtn.disabled = false;
        }
    }

    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
}

function cancelVote() {
    if (window.pollManager) {
        window.pollManager.cancelVote();
    }
}

function initPoll() {
    window.pollManager = new PollManager();
}

// Применяем ширины при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('poll-container')) {
        initPoll();
    }
});