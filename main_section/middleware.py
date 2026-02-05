from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import quote


import re

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Регулярные выражения для публичных URL
        self.public_patterns = [
            re.compile(r'^/login/$'),
            re.compile(r'^/register/$'),
            re.compile(r'^/logout/$'),
            re.compile(r'^/admin/login/$'),
            re.compile(r'^/test/$'), # Мало ли, проверю
            re.compile(r'^/static/'),
            re.compile(r'^/media/'),
            re.compile(r'^/captcha/'),  # ВСЕ URL с captcha
        ]

    def __call__(self, request):
        # Проверяем все регулярные выражения
        for pattern in self.public_patterns:
            if pattern.match(request.path):
                return self.get_response(request)

        if not request.user.is_authenticated:
            current_path = request.get_full_path()
            return redirect(f'{reverse("login")}?next={current_path}')

        return self.get_response(request)