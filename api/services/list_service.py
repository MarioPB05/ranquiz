from api.models import List


def get_list(share_code):
    """Función que devuelve el objeto "lista" al que pertenece el sharecode"""
    try:
        list_result = List.objects.get(share_code=share_code)
        return list_result
    except List.DoesNotExist:
        return None
