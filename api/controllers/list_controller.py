from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.models.list import List
from api.services.list_service import get_lists


@require_GET
def get_list_types(request):
    """Controlador que devuelve los tipos de listas"""
    list_types = List.TYPE_CHOICES
    result = []

    for list_type in list_types:
        result.append({
            'id': list_type[0],
            'text': list_type[1]
        })

    return JsonResponse({'types': result})


@require_GET
def get_lists_filtered(request):
    """Controlador que devuelve las listas"""
    page = int(request.GET.get('page', '1'))
    limit = 30
    sort = request.GET.get('sort', 'default')
    search = request.GET.get('search', '')
    result = []

    lists = get_lists(limit, page, search, request.user, sort)

    # TODO: Cambiar URL por la de list details
    for list_obj in lists:
        result.append({
            'id': list_obj['id'],
            'name': list_obj['name'],
            'image':  f"https://res.cloudinary.com/dhewpzvg9/{list_obj['image']}" if list_obj['image'] else None,
            'url': '/',
            'liked': list_obj['liked'],
            'plays': list_obj['plays'],
            'highlighted': list_obj['highlighted'],
            'author': {
                'username': list_obj['owner_username'],
                'avatar':  f"https://res.cloudinary.com/dhewpzvg9/{list_obj['owner_avatar']}",
                'url': request.build_absolute_uri(reverse('user', args=[list_obj['owner_share_code']])),
            }
        })

    return JsonResponse({'lists': result})
