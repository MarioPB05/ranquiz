from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.user_service import get_user, get_users


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
            'followers': user['followers'],
            'followed': user['followed'],
            'lists': user['lists'],
            'url': request.build_absolute_uri(reverse('user', args=[user["share_code"]]))
        })

    return JsonResponse({'users': result})
