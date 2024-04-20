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


def like_list(request, share_code):
    list_instance = get_object_or_404(List, share_code=share_code)

    # Verificar si el usuario ya ha dado like a la lista
    if ListLike.objects.filter(user=request.user, list=list_instance).exists():
        return JsonResponse({'message': 'Ya has dado like a esta lista'}, status=400)

    # Crear una nueva instancia de ListLike
    ListLike.objects.create(user=request.user, list=list_instance)

    return JsonResponse({'message': 'Like registrado exitosamente'})