def get_device_type(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    mobile_keywords = ['mobile', 'android', 'iphone']
    # tablet_keywords = ['ipad', 'tablet']

    if any(keyword in user_agent for keyword in mobile_keywords):
        return 'mobile'
    # elif any(keyword in user_agent for keyword in tablet_keywords):
    #     return 'tablet'
    else:
        return 'desktop'