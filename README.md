# Russian description

**Yurden Studio** — это веб-сайт, созданный для поддержки деятельности любительского переводческого коллектива. Проект представляет собой персональный сайт-визитку, который объединяет функционал для публикации переведённых глав манги, новостей студии и взаимодействия с читателями.

Этот репозиторий может служить примером моей работы как fullstack-разработчика: от проектирования структуры данных до реализации интерфейса «читалки».

## 🚀 Функциональность

*   **Библиотека и «Читалка» манги:**
    *   Каталог переводимых тайтлов.
    *   Удобный просмотр глав с поддержкой **полистного отображения** и режима **«разворот» (double-версия)** для планшетов и ПК.
    *   Адаптивный интерфейс для комфортного чтения на разных устройствах.
*   **Новостной раздел (блог):**
    *   Публикация новостей, анонсов и обновлений от студии.
    *   Система комментариев для обсуждения с читателями.
*   **Интерактивные элементы:**
    *   Раздел с опросами (`poll_section`) для сбора мнений аудитории (например, выбор следующего тайтла для перевода).

## 🛠 Стек технологий

*   **Backend:** Python, Django
*   **Frontend:** HTML, CSS, JavaScript, HTMX
*   **База данных:** SQLite (разработка), возможность лёгкого перехода на PostgreSQL
*   **Версионный контроль:** Git

## 📁 Структура проекта (основные директории)

*   `manga_section/` — приложение для управления тайтлами и главами манги.
*   `post_section/` — приложение для постов и комментариев.
*   `poll_section/` — приложение для создания и проведения опросов.
*   `static/` — статические файлы (CSS, JS, изображения для оформления).
*   `templates/` — HTML-шаблоны проекта.
*   `studio_new/` — основная конфигурация Django-проекта.
*   `media/` — пользовательский контент (в том числе страницы манги).

## 💡 Моя роль в проекте

Я являюсь единственным разработчиком этого проекта. Мною были выполнены следующие задачи:

1.  **Проектирование архитектуры:** Создал структуру базы данных для хранения информации о тайтлах, главах, страницах, пользовательских комментариях и голосованиях.
2.  **Разработка «читалки»:** Реализовал механизм отображения страниц манги, включая поддержку двух режимов чтения (по одной странице и разворотом), что потребовало нестандартной frontend-логики.
3.  **Итеративные улучшения:** Вёл активную работу над дизайном и юзабилити, что отражено в истории коммитов (например, переработка главной страницы, исправления вёрстки).
4.  **Полный цикл разработки:** Проект создавался с нуля и развивался, включая работу с миграциями базы данных, администрирование и отладку

# English description

**Yurden Studio** is a personal portfolio project – a dedicated website created for an amateur manga translation group. It serves as a hub for publishing translated manga chapters, studio news, and interacting with readers.

This repository showcases my skills as a full-stack developer, demonstrating the entire process from database design to implementing a custom manga reader interface.

## 🚀 Key Features

*   **Manga Library & Reader:**
    *   A catalog of ongoing translation projects.
    *   A custom-built reader with two viewing modes: **single-page** and **double-page spread**, enhancing the reading experience on tablets and desktops.
    *   Responsive design ensuring comfortable reading across all devices.
*   **News/Blog Section:**
    *   A blog to post announcements, updates, and other news from the studio.
    *   Integrated comment system to foster community discussion.
*   **Interactive Elements:**
    *   A polling feature (`poll_section`) to gather audience feedback and engage readers in decisions like choosing the next project.

## 🛠 Tech Stack

*   **Backend:** Python, Django
*   **Frontend:** HTML, CSS, JavaScript, HTMX
*   **Database:** SQLite (development), designed for easy migration to PostgreSQL
*   **Version Control:** Git

## 📁 Project Structure (Core Directories)

*   `manga_section/` — Django app for managing manga titles, chapters, and pages.
*   `post_section/` — Django app for posts and user comments.
*   `poll_section/` — Django app for creating and managing polls.
*   `static/` — Static assets (CSS, JS, images).
*   `templates/` — HTML templates.
*   `studio_new/` — Main Django project configuration.
*   `media/` — User-uploaded content (including manga pages).

## 💡 My Contribution

As the sole developer of this project, I was responsible for its complete lifecycle:

1.  **Architecture Design:** Planned the database schema to efficiently store information about titles, chapters, pages, comments, and polls.
2.  **Custom "Manga Reader" Development:** Engineered the core reading interface, including the logic for toggling between single and double-page views, which required custom JavaScript and CSS integration.
3.  **Iterative Design & UX Improvements:** Continuously refined the user interface and experience, as reflected in the commit history (e.g., major homepage redesign, layout fixes).
4.  **End-to-End Development:** Managed the entire development process, from initial setup and database migrations to deployment preparation.
