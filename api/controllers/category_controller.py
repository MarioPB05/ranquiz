from django.http import JsonResponse

from api.services.category_service import get_all_categories, similarity, create_category


def validate_category(request, category_name):
    """Función para validar una categoría"""
    categories = get_all_categories()
    found_similar = False
    similar_categories = []
    similar_category = None

    for c in categories:
        if similarity(c.name, category_name) > 0.7:
            found_similar = True
            similar_categories.append({
                'percentage': similarity(c.name, category_name),
                'category': c
            })

    if similar_categories:
        # Obtenemos la categoría más similar
        similar_category = max(similar_categories, key=lambda x: x['percentage'])['category']

    return JsonResponse({
        'validate': not found_similar,
        'similar_category': {
            'id': similar_category.id,
            'name': similar_category.name
        } if similar_category else None
    })


def get_categories(request):
    """Función para obtener todas las categorías"""
    categories = get_all_categories()
    json_categories = []

    for category in categories:
        json_categories.append({
            'id': category.id,
            'name': category.name,
            'share_code': category.share_code
        })

    return JsonResponse({'categories': json_categories})


def add_category(request):
    """Función para crear una categoría"""
    if request.method == 'POST':
        # Creamos la categoría
        category = create_category(request.POST)

        if category is not None:
            return JsonResponse({'id': category.id})

        return JsonResponse({'id': None})

    return JsonResponse({'id': None})
