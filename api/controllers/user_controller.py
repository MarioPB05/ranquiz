from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.models import user
from api.services.user_service import get_user, get_users
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
    limit = 30
    sort = request.GET.get('sort', 'default')
    search = request.GET.get('search', '')
    result = []

    users = get_users(limit, page, search, sort, request.user)

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


@require_authenticated
def follow_user(request):
    """Controlador que permite seguir a un usuario"""
    # Obtener el ID del usuario al que se quiere seguir o dejar de seguir
    followed_user_id = request.GET.get('followedUserId')

    # Verificar si el usuario ya sigue al usuario objetivo
    is_following = User.objects.filter(follower=request.user, followed_id=followed_user_id).exists()

    # Si el usuario ya sigue al usuario objetivo, dejar de seguirlo.
    if is_following:
        User.objects.filter(follower=request.user, followed_id=followed_user_id).delete()
        return JsonResponse({'status': 'success', 'message': 'Unfollowed successfully'})
    else:
        # Si el usuario no sigue al usuario objetivo, seguirlo
        followed_user = User.objects.get(pk=followed_user_id)
        User.objects.create(follower=request.user, followed=followed_user)
        return JsonResponse({'status': 'success', 'message': 'Followed successfully'})