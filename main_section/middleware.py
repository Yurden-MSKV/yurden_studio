from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import quote


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(f"=== DEBUG Middleware ===")
        # print(f"Путь: {request.path}")
        # print(f"Полный путь: {request.get_full_path()}")
        # print(f"Авторизован: {request.user.is_authenticated}")

        # Публичные URL
        public_urls = [
            '/login/',
            '/register/',
            '/logout/',
            '/admin/login/',
        ]

        # ⚠️ ВАЖНО: Исключаем статические и медиа файлы из проверки аутентификации
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        if not request.user.is_authenticated and request.path not in public_urls:
            # Получаем текущий путь
            current_path = request.get_full_path()
            # Перенаправляем на логин с параметром next
            return redirect(f'{reverse("login")}?next={current_path}')

        return self.get_response(request)