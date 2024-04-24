from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from api.services import category_service
from api.services.category_service import get_all_categories, similarity, create_category


@require_GET
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


@require_GET
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


@require_GET
def get_categories_filtered(request):
    """Función para obtener las categorías filtradas"""
    page = int(request.GET.get('page', '1'))
    limit = 30
    sort = request.GET.get('sort', 'default')
    search = request.GET.get('search', '')
    result = []

    categories = category_service.get_categories(limit, page, search, request.user, sort)

    # TODO: Cambiar URL por la de category view
    print(categories)
    for category in categories:
        result.append({
            'id': category['id'],
            'name': category['name'],
            'url': '/',
            'lists': category['lists'],
            'followers': category['followers'],
            'followed': category['followed']
        })

    return JsonResponse({'categories': result})


@require_POST
def add_category(request):
    """Función para crear una categoría"""
    category = create_category(request.POST)

    if category is not None:
        return JsonResponse({'id': category.id})

    return JsonResponse({'id': None})
