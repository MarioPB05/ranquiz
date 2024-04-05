from django.shortcuts import render

from api.services.user_service import user_login


def homepage(request):
    return render(request, 'pages/index.html')


def login(request):
    """Vista que permite a un usuario iniciar sesión en la aplicación"""
    form = user_login(request)
    return render(request, 'pages/login.html', {'form': form})


def create_list(request):
    """Vista que permite a un usuario crear una lista"""
    return render(request, 'pages/manage_list.html')
