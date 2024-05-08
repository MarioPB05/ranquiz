import cloudinary
from cloudinary import uploader  # skipcq: PY-W2000
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from api.models import List, ListCategory, ListFavorite, ListLike, ListAnswer
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.category_service import edit_list_categories, get_category, user_followed_category, \
    user_follow_category_and_receive_notifications
from api.services.get_service import get_user
from api.services.item_service import (
    create_item_form,
    create_item,
    edit_list_items,
    get_items,
)
from api.services.list_service import (
    create_list_form,
    create_list,
    get_list,
    get_list_counts, get_lists, count_lists,
)
from api.services.user_service import (
    user_login,
    user_register,
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
    list_data = get_list(share_code)
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
    favorites_count, likes_count, play_count = get_list_counts(list_data)

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
    list_obj = get_list(share_code)

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
        list_obj = get_list(share_code)
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


@partial_login_required
def profile(request, share_code=None):
    """Vista que renderiza el perfil de un usuario"""
    current_card = request.GET.get('card', 'resume')
    card_template = 'pages/profile/' + current_card + '.html'
    cards_info = {
        'resume': bool(current_card == 'resume'),
        'lists': bool(current_card == 'lists'),
        'quests': bool(current_card == 'quests'),
        'notifications': bool(current_card == 'notifications'),
        'settings': bool(current_card == 'settings'),
    }

    is_own_profile = share_code is None or request.user.share_code == share_code
    user_data = request.user if is_own_profile else get_user(share_code=share_code)

    if user_data is None:
        raise Http404('User not found')

    return render(request, 'pages/profile.html', {
        'user_data': user_data,
        'share_code': request.user.share_code if is_own_profile else share_code,
        'is_own_profile': is_own_profile,
        'card_template': card_template,
        'cards_info': cards_info,
    })


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
