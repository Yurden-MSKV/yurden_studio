def mobile_context(request):
    return {
        'is_mobile': getattr(request, 'is_mobile', False),
        'is_pc': getattr(request, 'is_pc', True)
    }