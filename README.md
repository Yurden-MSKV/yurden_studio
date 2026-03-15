**🌐 Языки / Languages:**
- [English](README.md)
- [Русский](README.ru.md)

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

*   **Backend:** Python, Django (including Migrations, Admin Panel)
*   **Frontend:** HTML, CSS, JavaScript (used for dynamic reader features)
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
