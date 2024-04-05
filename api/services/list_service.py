from api.models import List


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