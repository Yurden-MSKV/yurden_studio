class MobileDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        mobile_keywords = [
            'mobile', 'android', 'iphone', 'ipod', 'blackberry',
            'webos', 'opera mini', 'windows phone', 'iemobile'
        ]

        request.is_mobile = any(keyword in user_agent for keyword in mobile_keywords)
        request.is_pc = not request.is_mobile

        response = self.get_response(request)
        return response