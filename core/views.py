import cloudinary
from cloudinary import uploader
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from api.models import List
from api.services.category_service import get_category
from api.services.item_service import create_item_form, create_item, get_item
from api.services.list_service import create_list_form, set_category, create_list, get_list
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

            # Obtén todos los elementos existentes en la base de datos que pertenecen a la lista actual
            existing_items = list_obj.item_set.all()

            for item in existing_items:
                # Verifica si el prefijo del elemento existe en los elementos recibidos del formulario
                if str(item.id) not in items_prefix:
                    # Si el elemento existe en la base de datos pero no en la lista actual, elimínalo
                    cloudinary.uploader.destroy(item.image.public_id, invalidate=True)
                    item.delete()

            # Itera sobre cada prefijo de elemento recibido del formulario
            for prefix in items_prefix:
                item = get_item(prefix)

                # Verifica si corresponde a un elemento existente en la base de datos
                if item is not None and item.list == list_obj and item.id == int(prefix):
                    # Compara los datos del formulario con los datos existentes en la base de datos
                    if item.name != request.POST[f'{prefix}-name'] or item.image != request.FILES.get(
                            f'{prefix}-image'):
                        # Actualiza los datos del elemento existente en la base de datos
                        item.name = request.POST[f'{prefix}-name']

                        # Verifica si la imagen del elemento ha cambiado y la elimina de Cloudinary
                        if item.image and request.FILES.get(f'{prefix}-image') != item.image:
                            cloudinary.uploader.destroy(item.image.public_id, invalidate=True)

                        item.image = request.FILES.get(f'{prefix}-image')
                        item.save()
                else:
                    # Si no existe un elemento correspondiente en la base de datos, crea un nuevo elemento en la lista
                    item_form = create_item_form(request, prefix=prefix)
                    new_item = create_item(item_form)

                    if item_form.is_valid() and new_item is not None:
                        new_item.list = list_obj
                        new_item.save()

            # Elimina las categorías existentes de la lista antes de añadir las nuevas
            list_obj.listcategory_set.all().delete()

            if categories_names is not None:
                for category_name in categories_names:
                    category = get_category(category_name=category_name)

                    if category is not None:
                        set_category(list_obj, category)

        return redirect("/", list_id=list_obj.id)

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
