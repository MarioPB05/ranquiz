from api.models import Item, List, User


def get_item(item_id=None):
    """Función para obtener un item"""

    if item_id is not None:
        return Item.objects.get(id=item_id)

    return None


def get_list(share_code):
    """Función que devuelve el objeto "lista" al que pertenece el share code"""
    try:
        return List.objects.get(share_code=share_code)
    except List.DoesNotExist:
        return None


def get_user(user_id=None, share_code=None):
    """Función que obtiene un usuario por su id o su share_code"""
    try:
        if user_id is not None:
            return User.objects.get(id=user_id)

        if share_code is not None:
            return User.objects.get(share_code=share_code)

        return None
    except User.DoesNotExist:
        return None
