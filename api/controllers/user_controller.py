from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.user_service import get_user, get_users, toggle_user_follow
from api.models.user import User


@require_GET
@require_authenticated
def get_user_data(request):
    """Controlador que devuelve los datos del usuario"""
    user = get_user(request.user.id)

    return JsonResponse({'user': {
        'money': user.money,
        'avatar': f"https://res.cloudinary.com/dhewpzvg9/{user.avatar.image}",
    }})


@require_GET
def get_users_filtered(request):
    """Controlador que devuelve los usuarios filtrados"""
    page = int(request.GET.get('page', '1'))
    sort = request.GET.get('sort', 'default')
    search = request.GET.get('search', '')
    result = []

    users = get_users(PAGINATION_ITEMS_PER_PAGE, page, search, sort, request.user)

    for user in users:
        result.append({
            'id': user["id"],
            'username': user["username"],
            'avatar': f"https://res.cloudinary.com/dhewpzvg9/{user['avatar']}",
            'share_code': user['share_code'],
            'followers': user['followers'],
            'followed': user['followed'],
            'lists': user['lists'],
            'url': request.build_absolute_uri(reverse('user', args=[user["share_code"]]))
        })

    return JsonResponse({'users': result})


@require_authenticated
def follow_user(request, share_code):
    """Controlador que permite seguir o dejar de seguir a un usuario"""
    followed_user = get_user(share_code=share_code)

    if followed_user is None:
        return JsonResponse({'status': 'error', 'message': 'El usuario al que intentas seguir no existe'}, status=404)

    result = 'success' if toggle_user_follow(request.user, followed_user) else 'error'
    return JsonResponse({'status': result})