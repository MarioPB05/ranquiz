from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from api.models import ListLike
from api.models.list import List


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


from django.http import JsonResponse


def like_list(request, share_code):
    is_liked = request.POST.get('is_liked') == 'true'  # Convertir la cadena en un booleano

    if is_liked:
        # Si ya está "liked", eliminar el like si existe
        ListLike.objects.filter(user=request.user, list__share_code=share_code).delete()
        return JsonResponse({'message': 'Like eliminado exitosamente'})
    else:
        # Si no está "liked", agregar el like
        list_instance, _ = List.objects.get_or_create(share_code=share_code)
        ListLike.objects.create(user=request.user, list=list_instance)
        return JsonResponse({'message': 'Like registrado exitosamente'})
