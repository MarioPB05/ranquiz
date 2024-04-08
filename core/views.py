from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.services.item_service import create_item_form
from api.services.list_service import create_list_form
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


@login_required
def create_list(request):
    """Vista que permite a un usuario crear una lista"""
    list_form = create_list_form(request)
    item_form = create_item_form(request, prefix='template')

    return render(request, 'pages/manage_list.html', {
        'list_form': list_form,
        'item_form': item_form
    })
