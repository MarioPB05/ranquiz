from api.forms.list_form import CreateListForm
from api.models import List, ListCategory


def create_list_form(request):
    """Obtiene el formulario para crear una lista"""
    return CreateListForm(request.POST, request.FILES) if request.method == 'POST' else CreateListForm()


def create_list(list_form):
    """Función que crea una lista"""
    if list_form.is_valid():
        return list_form.save(commit=False)

    return None


def get_list(share_code):
    """Función que devuelve el objeto "lista" al que pertenece el sharecode"""
    try:
        return List.objects.get(share_code=share_code)
    except List.DoesNotExist:
        return None


def set_category(list_obj, category):
    """Función que añade una categoría a una lista"""
    list_category = ListCategory(list=list_obj, category=category)
    list_category.save()

    return list_category
