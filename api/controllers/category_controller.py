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
