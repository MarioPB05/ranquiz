from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from api.decorators.api_decorators import require_authenticated
from api.services import PAGINATION_ITEMS_PER_PAGE, category_service
from api.services.category_service import get_all_categories, similarity, create_category, user_follow_category, \
    get_category


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
    sort = request.GET.get('sort', 'default')
    search = request.GET.get('search', '')
    result = []

    categories = category_service.get_categories(PAGINATION_ITEMS_PER_PAGE, page, search, request.user, sort)

    for category in categories:
        result.append({
            'id': category['id'],
            'name': category['name'],
            'url': request.build_absolute_uri(reverse('category_lists', args=[category['share_code']])),
            'share_code': category['share_code'],
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


@require_GET
@require_authenticated
def follow_category(request, share_code):
    """Función para seguir una categoría"""
    follow = request.GET.get('follow', 'true') == 'true'
    notification = request.GET.get('notification', 'true') == 'true'
    category = get_category(share_code=share_code)

    if category is not None:
        result = user_follow_category(request.user, category, follow, notification)

        if result:
            return JsonResponse({'status': 'success', 'followed': follow, 'notification': notification})

    return JsonResponse({'status': 'error', 'message': 'Categoría no encontrada'})
