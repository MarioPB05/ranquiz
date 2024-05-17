
import cloudinary
from cloudinary import uploader  # skipcq: PY-W2000
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from api import sec_to_time
from api.models import List, ListCategory, ListFavorite, ListLike, ListAnswer, User
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.category_service import (edit_list_categories, get_category, get_user_categories,
                                           user_followed_category, user_follow_category_and_receive_notifications)
from api.services.goal_service import get_user_active_daily_goals
from api.services.item_service import (
    create_item_form,
    create_item,
    edit_list_items,
    get_items,
)
from api.services.list_service import (
    create_list_form,
    create_list,
    get_list_counts, get_lists, count_lists, get_user_lists_pagination, get_user_results, get_user_results_pagination
)
from api.services.list_service import get_user_lists
from api.services.shop_service import highlight_list
from api.services.user_service import (
    user_login,
    user_register,
    get_user_stats, get_users_following, get_users_followers
)
from core.decorators.decorators import partial_login_required


def homepage(request):
    """Vista que renderiza la página de inicio de la aplicación"""
    return render(request, 'pages/index.html')


def login(request):
    """Vista que permite a un usuario iniciar sesión en la aplicación"""
    return user_login(request)


def register(request):
    """Vista que permite a un usuario registrarse en la aplicación"""
    return user_register(request)


def logout(request):
    """Vista que permite a un usuario cerrar sesión en la aplicación"""
    django_logout(request)
    return redirect('login')


def list_details(request, share_code):
    """Vista que permite a un usuario ver los detalles de una lista"""
    try:
        list_data = List.get(share_code)
    except List.DoesNotExist:
        return HttpResponseNotFound()

    items_data = get_items(share_code)

    # Comprueba si la lista no ha sido eliminada
    if list_data.deleted and list_data.owner != request.user:
        return HttpResponseNotFound()

    # Comprueba si la lista es privada y si el usuario tiene permiso para verla
    if list_data.public == 0 and list_data.owner != request.user:
        return HttpResponseForbidden()

    # Obtener todas las instancias de ListCategory asociadas a la lista específica
    list_categories = ListCategory.objects.filter(list=list_data)

    # Obtener las instancias de Category a partir de las instancias de ListCategory
    categories = [list_category.category for list_category in list_categories]

    # Obtener la cantidad de favoritos, likes, partidas de la lista
    favorites_count, likes_count, play_count, comments_count = get_list_counts(list_data)  # skipcq: PYL-W0612

    # Verificar si el usuario ha dado like, favorito o jugado a la lista específica
    user_has_liked = False
    user_has_favorited = False
    user_has_played = False
    if request.user.is_authenticated:
        user_has_liked = ListLike.objects.filter(user=request.user, list=list_data).exists()
        user_has_favorited = ListFavorite.objects.filter(user=request.user, list=list_data).exists()
        user_has_played = ListAnswer.objects.filter(user=request.user, list=list_data).exists()

    data = {
        "name": list_data.name,
        "owner": list_data.owner.username,
        "owner_sharecode": list_data.owner.share_code,
        "elements": len(items_data),
        "creation_date": list_data.creation_date,
        "edit_date": list_data.edit_date,
        "avatar": list_data.owner.avatar.image,
        "categories": categories,
        "favorites_count": favorites_count,
        "likes_count": likes_count,
        "play_count": play_count,
        "user_has_liked": user_has_liked,
        "user_has_favorited": user_has_favorited,
        "user_has_played": user_has_played,
    }

    return render(request, 'pages/list_details.html', {'share_code': share_code, 'list': list_data, "data": data})


def play_list(request, share_code):
    """Vista que permite a un usuario jugar una lista"""
    list_obj = List.get(share_code)

    # Comprueba si la lista no ha sido eliminada
    if list_obj is None or list_obj.deleted:
        return HttpResponseNotFound()

    # Comprueba si la lista es privada y si el usuario tiene permiso para verla
    if list_obj.public == 0 and list_obj.owner != request.user:
        return HttpResponseForbidden()

    return render(request, 'pages/play_list.html', {'share_code': share_code, 'list': list_obj})


@login_required
def create_list_view(request):
    """Vista que permite a un usuario crear una lista"""
    list_form = create_list_form(request)
    item_form = create_item_form(request, prefix='template')

    if request.method == 'POST' and list_form.is_valid():
        list_obj = create_list(list_form)
        list_obj.owner = request.user
        list_obj.public = bool(request.POST.get('visibility') == 'public')

        items_prefix = request.POST.get('items_prefix').split(',')
        categories_names = request.POST.get('categories').split(',')

        if list_obj is not None and len(items_prefix) > 0:
            list_obj.type = 0
            list_obj.save()

            if request.POST.get('range_date_highlight') is not None and request.POST.get('range_date_highlight') != '':
                dates = request.POST.get('range_date_highlight').split(' hasta ')
                start_date = dates[0]
                end_date = dates[0] if len(dates) == 1 else dates[1]

                highlight_list(request.user, list_obj.share_code, start_date, end_date)

            for prefix in items_prefix:
                item_form = create_item_form(request, prefix=prefix)
                item = create_item(item_form)

                if item_form.is_valid() and item is not None:
                    item.list = list_obj
                    item.save()

            edit_list_categories(categories_names, list_obj)
            return redirect('list_details', share_code=list_obj.share_code)

    return render(request, 'pages/manage_list.html', {
        'list_form': list_form,
        'item_form': item_form,
        'edit_mode': False
    })


@login_required
def edit_list_view(request, share_code):
    """Vista que permite a un usuario editar una lista existente"""
    list_obj = get_object_or_404(List, share_code=share_code)

    # Comprueba si el usuario tiene permiso para editar la lista
    if list_obj.owner != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta lista")

    # Crea el formulario de lista con los datos de la lista existente
    list_form = create_list_form(request, instance=list_obj)
    item_form = create_item_form(request, prefix='template')

    if request.method == 'POST' and list_form.is_valid():
        # Actualiza los datos de la lista con los datos del formulario
        list_obj = List.get(share_code)
        list_obj.name = request.POST.get('name')
        list_obj.question = request.POST.get('question')
        list_obj.public = bool(request.POST.get('visibility') == 'public')

        # Verifica si la foto de la lista ha cambiado y la elimina de Cloudinary
        if 'image' in request.FILES:
            new_image = request.FILES['image']
            if new_image != list_obj.image:
                if list_obj.image:
                    cloudinary.uploader.destroy(list_obj.image.public_id, invalidate=True)

                list_obj.image = new_image

        items_prefix = request.POST.get('items_prefix').split(',')
        categories_names = request.POST.get('categories').split(',')

        if len(items_prefix) > 0:
            list_obj.type = 0
            list_obj.save()

            edit_list_items(items_prefix, list_obj, request)
            edit_list_categories(categories_names, list_obj)

        return redirect('list_details', share_code=list_obj.share_code)

    item_form_set = []

    for item in list_obj.item_set.all():
        item_form = create_item_form(request, prefix=item.id, instance=item)
        item_form_set.append(item_form)

    return render(request, 'pages/manage_list.html', {
        'item_form_set': item_form_set,
        'list_form': list_form,
        'item_form': item_form,
        'edit_mode': True
    })


def profile_resume(request, user_data, card_data):
    """Vista que renderiza el resumen de un usuario"""
    page_number = int(request.GET.get('page', 1))
    user_lists = get_user_lists(user_data, False, 'public', None, page_number)
    user_categories = get_user_categories(user_data, page_number)
    user_favourite_lists = get_user_lists(user_data, False, 'favourite', None, page_number)
    users_following = get_users_following(user_data, request.user, page_number)
    users_followers = get_users_followers(user_data, request.user, page_number)

    card_data['data'] = {
        'categories': [],
        'published': [],
        'favorites': [],
        'following': [],
        'followers': [],
    }

    for user_category in user_categories:
        card_data['data']['categories'].append({
            'user': user_category['name'],
            'share_code': user_category['share_code'],
            'lists': user_category['lists'],
            'followers': user_category['followers']
            if request.user.is_authenticated else False
        })

    for user_list in user_lists:
        card_data['data']['published'].append({
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
        })

    for user_favourite_list in user_favourite_lists:
        card_data['data']['favorites'].append({
            'name': user_favourite_list['name'],
            'highlighted': user_favourite_list['highlighted'] == 1,
            'image': user_favourite_list['image'] if user_favourite_list['image'] else None,
            'share_code': user_favourite_list['share_code'],
            'plays': user_favourite_list['plays'],
            'owner_username': user_favourite_list['owner_username'],
            'owner_avatar': user_favourite_list['owner_avatar'],
            'owner_share_code': user_favourite_list['owner_share_code'],
            'liked': ListLike.objects.filter(user=request.user, list_id__exact=user_favourite_list['id']).exists()
            if request.user.is_authenticated else False
        })

    for user_following in users_following:
        card_data['data']['following'].append({
            'name': user_following['username'],
            'image': user_following['avatar'],
            'share_code': user_following['share_code'],
            'followers': user_following['followers'],
            'followed': user_following['followed'],
            'lists': user_following['lists']
        })

    for user_follower in users_followers:
        card_data['data']['followers'].append({
            'name': user_follower['username'],
            'image': user_follower['avatar'],
            'share_code': user_follower['share_code'],
            'followers': user_follower['followers'],
            'followed': user_follower['followed'],
            'lists': user_follower['lists']
        })


def profile_lists(request, user_data, card_data):
    """Vista que renderiza las listas de un usuario"""
    page_number = int(request.GET.get('page', 1))
    search_query = request.GET.get('search', None)
    visibility = request.GET.get('visibility', None)
    show_deleted = request.GET.get('show_deleted', 'false') == 'true'

    user_lists = get_user_lists(user_data, show_deleted, visibility, search_query, page_number)
    count_user_lists = get_user_lists_pagination(user_data, show_deleted, visibility, search_query, page_number)

    card_data['pagination'] = count_user_lists
    card_data['searching'] = search_query is not None
    card_data['visibility'] = visibility
    card_data['show_deleted'] = show_deleted
    card_data['search_query'] = search_query

    for user_list in user_lists:
        card_data['data'].append({
            'name': user_list['name'],
            'highlighted': user_list['highlighted'] == 1,
            'image': f"https://res.cloudinary.com/dhewpzvg9/{user_list['image']}" if user_list['image'] else None,
            'public': user_list['public'],
            'deleted': user_list['deleted'],
            'date': user_list['creation_date'],
            'share_code': user_list['share_code'],
            'play_count': user_list['plays'],
            'likes_count': user_list['likes'],
            'comments_count': user_list['comments'],
            'favorites_count': user_list['favorites']
        })


def profile_results(request, user_data, card_data):
    """Vista que renderiza los resultados de un usuario"""
    page_number = int(request.GET.get('page', 1))
    search_query = request.GET.get('search', None)
    list_share_code = request.GET.get('list', None)
    list_obj = None

    if list_share_code is not None:
        list_obj = List.get(list_share_code)
        if list_obj is None:
            raise Http404('List not found')

    user_results = get_user_results(user_data, list_obj, page_number, search_query)
    count_user_results = get_user_results_pagination(user_data, list_obj, page_number, search_query)

    card_data['pagination'] = count_user_results
    card_data['searching'] = search_query is not None
    card_data['search_query'] = search_query
    card_data['list'] = list_obj.share_code if list_obj is not None else None
    card_data['selected_list'] = list_obj

    for user_result in user_results:
        card_data['data'].append({
            'list_name': user_result['list_name'],
            'list_image': f"https://res.cloudinary.com/dhewpzvg9/{user_result['list_image']}"
            if user_result['list_image'] else None,
            'start_date': user_result['start_date'],
            'items': user_result['items'],
            'duration': sec_to_time(user_result['duration']),
        })


def profile_quests(request, user_data, card_data):
    """Vista que renderiza las misiones de un usuario"""
    goals = get_user_active_daily_goals(user_data)

    for userGoal in goals:
        card_data['data'].append({
            'id': userGoal.goal.id,
            'name': userGoal.goal.id_type.title,
            'progress': userGoal.progress,
            'goal': userGoal.goal.value,
            'reward': userGoal.goal.reward,
            'claimed': userGoal.claimed,
            'percentage': str(round((userGoal.progress / userGoal.goal.value) * 100, 2)).replace(',', '.')
        })


@partial_login_required
def profile(request, share_code=None):
    """Vista que renderiza el perfil de un usuario"""
    current_card = request.GET.get('card', 'resume')
    card_template = 'pages/profile/' + current_card + '.html'
    cards = ('resume', 'lists', 'quests', 'results', 'notifications', 'settings')

    user_share_code = request.user.share_code if request.user.is_authenticated else None
    is_own_profile = share_code is None or user_share_code == share_code
    user_data = request.user if is_own_profile else User.get(share_code=share_code)

    if user_data is None:
        raise Http404('User not found')

    if current_card not in cards:
        raise Http404('Page not found')

    user_stats = get_user_stats(user_data)

    card_data = {'data': []}
    if current_card == 'resume':
        profile_resume(request, user_data, card_data)
    elif current_card == 'lists':
        profile_lists(request, user_data, card_data)
    elif current_card == 'results':
        profile_results(request, user_data, card_data)
    elif current_card == 'quests':
        profile_quests(request, user_data, card_data)

    return render(request, 'pages/profile.html', {
        'user_data': user_data,
        'user_stats': user_stats,
        'share_code': user_share_code if is_own_profile else share_code,
        'is_own_profile': is_own_profile,
        'card_template': card_template,
        'current_card': current_card,
        'card_data': card_data,
        'card_data_empty': len(card_data['data']) == 0,
        'current_path': request.get_full_path_info(),
    })


@login_required
def shop(request):
    """Vista que renderiza la tienda de la aplicación"""
    return render(request, 'pages/shop.html')


def search(request):
    """Vista que permite a un usuario buscar en la aplicación"""
    return render(request, 'pages/search.html')


def category_lists(request, share_code):
    """Vista que renderiza las listas de una categoría específica"""
    page = int(request.GET.get('page', 1))
    order = request.GET.get('order', 'default')
    category_object = get_category(share_code=share_code)
    lists = get_lists(PAGINATION_ITEMS_PER_PAGE, page, user=request.user, order=order, category=category_object)
    list_count = count_lists(category=category_object)[0]['count']
    page_numbers = list(range(page - 1, list_count // PAGINATION_ITEMS_PER_PAGE + 2))

    if 0 in page_numbers:
        page_numbers.remove(0)

    if len(page_numbers) > 6:
        page_numbers = page_numbers[:6]

    return render(request, 'pages/category_lists.html', {
        'share_code': share_code,
        'lists': lists,
        'category': category_object,
        'followed': user_followed_category(request.user, category_object),
        'notifications': user_follow_category_and_receive_notifications(request.user, category_object),
        'order': order,
        'user': request.user,
        'pagination': {
            'total_pages': list_count // PAGINATION_ITEMS_PER_PAGE + 1,
            'current_page': page,
            'items_per_page': PAGINATION_ITEMS_PER_PAGE,
            'page_numbers': page_numbers
        }
    })
