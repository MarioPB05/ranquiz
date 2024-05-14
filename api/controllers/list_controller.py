import json
from datetime import datetime

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from api.decorators.api_decorators import require_authenticated
from api.models.list import List
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.list_service import (get_lists, toggle_like_list, toggle_favorite_list, toggle_visibility_list,
                                       add_result, delete_list, recover_list)


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
    sort = request.GET.get('sort', 'default')
    search = request.GET.get('search', '')
    result = []

    lists = get_lists(PAGINATION_ITEMS_PER_PAGE, page, search, request.user, sort)

    for list_obj in lists:
        result.append({
            'id': list_obj['id'],
            'name': list_obj['name'],
            'image':  f"https://res.cloudinary.com/dhewpzvg9/{list_obj['image']}" if list_obj['image'] else None,
            'url': request.build_absolute_uri(reverse('list_details', args=[list_obj['share_code']])),
            'share_code': list_obj['share_code'],
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


@require_authenticated
def like_list(request, share_code):
    """Controlador que permite dar like a una lista"""
    result = 'success' if toggle_like_list(request.user, share_code) else 'error'
    return JsonResponse({'status': result})


@require_authenticated
def favorite_list(request, share_code):
    """Controlador que permite marcar una lista como favorita"""
    result = 'success' if toggle_favorite_list(request.user, share_code) else 'error'
    return JsonResponse({'status': result})


@csrf_exempt
@require_POST
@require_authenticated
def add_result_to_list(request, share_code):
    """Controlador que permite añadir un resultado a una lista"""
    result = request.POST.get('result')
    list_obj = List.get(share_code=share_code)
    start_date = request.POST.get('startDate')

    # Convertir de JSON a array
    result = json.loads(result)

    # Convertir de milisegundos a fecha y hora
    start_date = datetime.fromtimestamp(int(start_date) / 1000)

    result = add_result(request.user, list_obj, result, start_date)
    status = 'success' if result else 'error'

    if result:
        return JsonResponse({'status': status, 'result_id': result.id})

    return JsonResponse({'status': status})


@require_GET
@require_authenticated
def visibility_list(request, share_code):
    """Controlador que permite cambiar la visibilidad de una lista"""
    toggle_visibility_list(share_code)

    return JsonResponse({'status': 'success'})


@require_GET
@require_authenticated
def delete_or_recover_list(request, share_code):
    """Controlador que permite eliminar una lista"""
    result = 'success' if delete_list(share_code) else 'error'

    return JsonResponse({'status': result})


@require_GET
@require_authenticated
def recover_list_eliminated(request, share_code):
    """Controlador que permite recuperar una lista"""
    result = 'success' if recover_list(share_code) else 'error'

    return JsonResponse({'status': result})
