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


def profile(request, share_code):
    """Vista que renderiza el perfil de un usuario"""
    return render(request, 'pages/profile.html', {'share_code': share_code})
