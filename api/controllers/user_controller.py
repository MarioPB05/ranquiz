from django.http import JsonResponse

from api.services.user_service import get_user


def get_user_data(request):
    """Controlador que devuelve los datos del usuario"""
    if request.user.is_authenticated:
        user = get_user(request.user.id)

        return JsonResponse({'user': {
            'money': user.money,
            'avatar': f"https://res.cloudinary.com/dhewpzvg9/{user.avatar.image}",
        }})

    return JsonResponse({
        'status': 'error',
        'message': 'No se ha iniciado sesión en la aplicación'
    }, status=401)
