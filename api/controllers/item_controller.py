import cloudinary
from django.http import JsonResponse
from api.services.item_service import get_items


def get_current_items(request, share_code):
    """Función para obtener los items que no han sido eliminados de una lista"""
    items = get_items(share_code)
    result = []

    if not items:
        return JsonResponse({'items': result})

    for item in items:
        result.append({
            'id': item.id,
            'name': item.name,
            'image': cloudinary.CloudinaryImage.build_url(item.image) if item.image else None,
        })

    return JsonResponse({'items': result})


def get_all_items(request, share_code):
    """Función para obtener todos los items de una lista"""
    items = get_items(share_code, True)
    result = []

    if items is None:
        return JsonResponse({'status': 'error', 'message': 'Lista no encontrada'})

    for item in items:
        result.append({
            'id': item.id,
            'name': item.name,
            'image': cloudinary.CloudinaryImage.build_url(item.image) if item.image else None,
        })

    return JsonResponse({'items': result})
