from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.models import ListLike, ListFavorite
from api.models.list import List
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.list_service import get_lists, toggle_visibility_list, delete_list


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
    is_liked = request.GET.get('isLiked') == 'true'  # Convertir la cadena en un booleano

    if not is_liked:
        # Si ya está "liked", eliminar el like si existe
        ListLike.objects.filter(user=request.user, list__share_code=share_code).delete()
    else:
        # Si no está "liked", agregar el like
        list_instance, _ = List.objects.get_or_create(share_code=share_code)
        ListLike.objects.create(user=request.user, list=list_instance)

    return JsonResponse({'status': 'success'})


@require_authenticated
def favorite_list(request, share_code):
    """Controlador que permite marcar una lista como favorita"""
    is_favorited = request.GET.get('isFavorited') == 'true'  # Convertir la cadena en un booleano

    if not is_favorited:
        # Si ya está marcada como favorita, eliminar el favorito si existe
        ListFavorite.objects.filter(user=request.user, list__share_code=share_code).delete()
    else:
        # Si no está marcada como favorita, agregar el favorito
        list_instance, _ = List.objects.get_or_create(share_code=share_code)
        ListFavorite.objects.create(user=request.user, list=list_instance)

    return JsonResponse({'status': 'success'})


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
