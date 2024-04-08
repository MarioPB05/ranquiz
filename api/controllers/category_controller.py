import json

from django.core.serializers import serialize
from django.http import JsonResponse

from api.forms.category_form import CreateCategoryForm
from api.services.category_service import get_all_categories, similarity, create_category


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


def add_category(request):
    """Función para crear una categoría"""
    if request.method == 'POST':
        # Creamos la categoría
        category = create_category(request.POST)

        if category is not None:
            return JsonResponse({'id': category.id})
        else:
            return JsonResponse({'id': None})
