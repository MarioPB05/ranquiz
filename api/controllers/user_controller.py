from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.models import ListLike
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.list_service import get_user_lists
from api.services.user_service import get_user, get_users, toggle_user_follow


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


def user_lists(request, share_code):
    """Controlador que devuelve las listas de un usuario"""
    user_data = get_user(share_code=share_code)
    page_number = int(request.GET.get('page', 1))
    lists = get_user_lists(user_data, False, 'public', None, page_number)
    lists_html = []

    for user_list in lists:
        list_data = {
            'name': user_list['name'],
            'highlighted': user_list['highlighted'] == 1,
            'image': user_list['image'] if user_list['image'] else None,
            'share_code': user_list['share_code'],
            'plays': user_list['plays'],
            'owner_username': user_list['owner_username'],
            'owner_avatar': user_list['owner_avatar'],
            'owner_share_code': user_list['owner_share_code'],
            'liked': ListLike.objects.filter(user=request.user, list_id__exact=user_list['id']).exists()
            if request.user.is_authenticated else False
        }

        lists_html.append(render_to_string('components/list_template.html', {'data': list_data}))

    return JsonResponse({'lists': lists_html})
