from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from api.models import ListCategory
from api.services.category_service import get_category
from api.services.item_service import get_items
from api.services.list_service import get_list
from api.services.item_service import create_item_form, create_item
from api.services.list_service import create_list_form, set_category, create_list
from api.services.user_service import user_login, user_register, get_user
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

    # Obtener todas las instancias de ListCategory asociadas a la lista específica
    list_categories = ListCategory.objects.filter(list=list_data)

    # Obtener las instancias de Category a partir de las instancias de ListCategory
    categories = [list_category.category for list_category in list_categories]

    data = {
        "name": list_data.name,
        "owner": list_data.owner.username,
        "owner_sharecode": list_data.owner.share_code,
        "elements": len(items_data),
        "creation_date": list_data.creation_date,
        "edit_date": list_data.edit_date,
        "avatar": list_data.owner.avatar.image,
        "categories": categories
    }
    return render(request, 'pages/list_details.html', {'share_code': share_code, 'list': list_data, "data": data})

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

            if categories_names is not None:
                for category_name in categories_names:
                    category = get_category(category_name=category_name)

                    if category is not None:
                        set_category(list_obj, category)

    return render(request, 'pages/manage_list.html', {
        'list_form': list_form,
        'item_form': item_form
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
