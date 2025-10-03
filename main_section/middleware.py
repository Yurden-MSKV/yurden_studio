from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Публичные URL
        public_urls = [
            reverse('login'),
            reverse('register'),
            reverse('logout'),
            '/admin/login/',
        ]

        # ⚠️ ВАЖНО: Исключаем статические и медиа файлы из проверки аутентификации
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        if not request.user.is_authenticated and request.path not in public_urls:
            return redirect('login')

        return self.get_response(request)