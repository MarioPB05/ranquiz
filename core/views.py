from django.shortcuts import render

from api.services.user_service import user_login, user_register


def homepage(request):
    """Vista que renderiza la página de inicio de la aplicación"""
    return render(request, 'pages/index.html')


def login(request):
    """Vista que permite a un usuario iniciar sesión en la aplicación"""
    return user_login(request)


def register(request):
    """Vista que permite a un usuario registrarse en la aplicación"""
    return user_register(request)


def list_details(request, share_code):
    """Vista que permite a un usuario ver los detalles de una lista"""
    return render(request, 'pages/list_details.html', {'share_code': share_code})