from api.models import List


def get_list(share_code):
    """Función que devuelve el objeto "lista" al que pertenece el sharecode"""
    try:
        return List.objects.get(share_code=share_code)
    except List.DoesNotExist:
        return None
