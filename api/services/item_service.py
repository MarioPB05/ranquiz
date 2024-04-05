from api.models import Item
from api.services.list_service import get_list


def create_item(item_form):
    """Función para crear un item"""

    if item_form.is_valid():
        # Guardamos el item y lo devolvemos
        return item_form.save(commit=False)
    else:
        return None


def get_items(share_code):
    """Función para obtener los items de una lista"""

    # Obtenemos la lista
    required_list = get_list(share_code)

    if required_list is None:
        return None

    # Obtenemos los items de la lista
    items = Item.objects.filter(list=required_list)

    return items
