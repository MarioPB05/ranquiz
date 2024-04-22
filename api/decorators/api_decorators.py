from functools import wraps

from django.http import HttpResponseForbidden, JsonResponse


def require_authenticated(function):
    """Decorador para requerir autenticación en la API"""
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden(JsonResponse({'error': 'No tienes permisos para acceder al recurso'}))
        return function(request, *args, **kwargs)
    return _wrapped_view
