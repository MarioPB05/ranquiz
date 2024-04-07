# from django.shortcuts import render

from api.forms.list_form import CreateListForm
from api.models import List
# from api.services.item_service import create_item_form


def create_list_form(request):
    """Obtiene el formulario para crear una lista"""
    return CreateListForm(request.POST) if request.method == 'POST' else CreateListForm()


def create_list(list_form):
    """Función que crea una lista"""
    if list_form.is_valid():
        return list_form.save(commit=False)
    else:
        return None


def get_list(share_code):
    """Función que devuelve el objeto "lista" al que pertenece el sharecode"""
    try:
        return List.objects.get(share_code=share_code)
    except List.DoesNotExist:
        return None


def create_list_view(request):
    pass
