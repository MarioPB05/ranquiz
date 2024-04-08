import json

from django.core.serializers import serialize
from django.http import JsonResponse

from api.services.category_service import get_all_categories, similarity


def validate_category(request, category_name):
    """Función para validar una categoría"""
    categories = get_all_categories()
    found_similar = False

    for c in categories:
        if similarity(c.name, category_name) > 0.7:
            found_similar = True
            break

    return JsonResponse({'validate': not found_similar})


def get_categories(request):
    """Función para obtener todas las categorías"""
    serialized_categories = serialize('json', get_all_categories())
    return JsonResponse({'categories': json.loads(serialized_categories)})
