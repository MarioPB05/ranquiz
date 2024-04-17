from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.services.user_service import get_user


@require_GET
@require_authenticated
def get_user_data(request):
    """Controlador que devuelve los datos del usuario"""
    user = get_user(request.user.id)

    return JsonResponse({'user': {
        'money': user.money,
        'avatar': f"https://res.cloudinary.com/dhewpzvg9/{user.avatar.image}",
    }})
