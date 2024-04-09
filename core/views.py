from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from api.models import List
from api.services.category_service import get_category
from api.services.item_service import create_item_form, create_item
from api.services.list_service import create_list_form, set_category, create_list
from api.services.user_service import user_login, user_register


def homepage(request):
    """Vista que renderiza la página de inicio de la aplicación"""
    return render(request, 'pages/index.html')


def login(request):
    """Vista que permite a un usuario iniciar sesión en la aplicación"""
    return user_login(request)


def register(request):
    """Vista que permite a un usuario registrarse en la aplicación"""
    return user_register(request)


@login_required
def create_list_view(request):
    """Vista que permite a un usuario crear una lista"""
    list_form = create_list_form(request)
    item_form = create_item_form(request, prefix='template')

    if request.method == 'POST' and list_form.is_valid():
        list_obj = create_list(list_form)
        list_obj.owner = request.user
        list_obj.public = True if request.POST.get('visibility') == 'public' else False

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
