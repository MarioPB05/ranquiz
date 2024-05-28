from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.models import ListLike, User
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.category_service import get_user_categories
from api.services.list_service import get_user_lists, get_user_favourite_lists
from api.services.notification_service import count_unread_notifications
from api.services.user_service import get_users, toggle_user_follow, get_users_following, get_users_followers, \
    generate_invitation_code


@require_GET
@require_authenticated
def get_user_data(request):
    """Controlador que devuelve los datos del usuario"""
    user = User.get(user_id=request.user.id)

    return JsonResponse({'user': {
        'money': user.money,
        'avatar': f"https://res.cloudinary.com/dhewpzvg9/{user.avatar.image}",
        'unread_notifications': count_unread_notifications(request.user),
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
    followed_user = User.get(share_code=share_code)

    if followed_user is None:
        return JsonResponse({'status': 'error', 'message': 'El usuario al que intentas seguir no existe'}, status=404)

    result = 'success' if toggle_user_follow(request.user, followed_user) else 'error'
    return JsonResponse({'status': result})


def user_lists(request, share_code):
    """Controlador que devuelve las listas de un usuario"""
    user_data = User.get(share_code=share_code)
    page_number = int(request.GET.get('page', 1))
    current_filter = request.GET.get('filter', 'default')

    if current_filter == 'default':
        lists = get_user_lists(user_data, False, 'public', None, page_number)
    elif current_filter == 'favorites':
        lists = get_user_favourite_lists(user_data, request.user, page_number)
    else:
        return JsonResponse({'lists': []})

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

    return JsonResponse({'results': lists_html})


def user_categories(request, share_code):
    """Controlador que devuelve las categorías de un usuario"""
    user_data = User.get(share_code=share_code)
    page_number = int(request.GET.get('page', 1))
    categories = get_user_categories(user_data, request.user, page_number)
    categories_html = []

    for category in categories:
        categories = {
            'user': category['name'],
            'share_code': category['share_code'],
            'lists': category['lists'],
            'followers': category['followers'],
            'followed': category['followed']
            if request.user.is_authenticated else False
        }

        categories_html.append(render_to_string('components/category_template.html', {'data': categories}))

    return JsonResponse({'results': categories_html})


def user_following(request, share_code):
    """Controlador que devuelve los seguidores de un usuario"""
    user_data = User.get(share_code=share_code)
    page_number = int(request.GET.get('page', 1))
    current_filter = request.GET.get('filter', 'followers')

    if current_filter == 'followers':
        followings = get_users_followers(user_data, request.user, page_number)
    elif current_filter == 'following':
        followings = get_users_following(user_data, request.user, page_number)
    else:
        return JsonResponse({'results': []})

    following_html = []

    for user in followings:
        follower_data = {
            'user': request.user,
            'name': user['username'],
            'image': user['avatar'],
            'share_code': user['share_code'],
            'followers': user['followers'],
            'followed': user['followed'],
            'lists': user['lists']
        }

        following_html.append(render_to_string('components/user_template.html', {'data': follower_data}))

    return JsonResponse({'results': following_html})


def generate_user_invitation_code(request):
    """Controlador que genera un código de invitación para un usuario"""
    return JsonResponse({'code': generate_invitation_code(request.user)})
