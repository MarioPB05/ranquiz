from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.services.user_service import user_login, user_register


def homepage(request):
    return render(request, 'pages/index.html')


def login(request):
    """Vista que permite a un usuario iniciar sesión en la aplicación"""
    return user_login(request)


def register(request):
    """Vista que permite a un usuario registrarse en la aplicación"""
    return user_register(request)


@login_required
def create_list(request):
    """Vista que permite a un usuario crear una lista"""
    return render(request, 'pages/manage_list.html')
