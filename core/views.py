from django.shortcuts import render

from api.services.user_service import user_login


def homepage(request):
    return render(request, 'pages/index.html')


def login(request):
    """Vista que permite a un usuario iniciar sesión en la aplicación"""
    form = user_login(request)
    return render(request, 'pages/login.html', {'form': form})


def register(request):
    """Vista que permite a un usuario registrarse en la aplicación"""
    return render(request, 'pages/register.html')


