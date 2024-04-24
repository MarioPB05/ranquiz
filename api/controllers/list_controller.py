from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.models import ListLike, ListFavorite
from api.models.list import List


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


@require_authenticated
def like_list(request, share_code):
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
    is_favorited = request.GET.get('isFavorited') == 'true'  # Convertir la cadena en un booleano

    if not is_favorited:
        # Si ya está marcada como favorita, eliminar el favorito si existe
        ListFavorite.objects.filter(user=request.user, list__share_code=share_code).delete()
    else:
        # Si no está marcada como favorita, agregar el favorito
        list_instance, _ = List.objects.get_or_create(share_code=share_code)
        ListFavorite.objects.create(user=request.user, list=list_instance)

    return JsonResponse({'status': 'success'})
