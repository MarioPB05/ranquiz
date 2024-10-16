from cloudinary import uploader

from api.forms.item_form import CreateItemForm
from api.models import List, Item, Notification
from api.models.notification_type import NotificationTypes


def create_item_form(request, prefix=None, instance=None):
    """Función para obtener el formulario de un item"""
    return CreateItemForm(request.POST, request.FILES, prefix=prefix, instance=instance) if request.method == 'POST' \
        else CreateItemForm(prefix=prefix, instance=instance)


def create_item(item_form):
    """Función para crear un item"""
    if item_form.is_valid():
        # Guardamos el item y lo devolvemos
        return item_form.save(commit=False)

    return None


def edit_list_items(items_prefix, list_obj, request):
    """Función para editar los items de una lista"""
    existing_items = list_obj.item_set.all()

    for item in existing_items:
        # Verifica si el prefijo del elemento existe en los elementos recibidos del formulario
        if str(item.id) not in items_prefix:
            # Si el elemento existe en la base de datos pero no en la lista actual, elimínalo
            if item.image is not None:
                uploader.destroy(item.image.public_id, invalidate=True)

            item.deleted = True
            item.save()

    if len(existing_items) != len(items_prefix) and len(items_prefix) > len(existing_items):
        # Se crearon nuevos elementos en la lista
        Notification.create(2, NotificationTypes.NEW_LIST_OPTIONS.object, list_obj.owner, list_obj.share_code)

    # Itera sobre cada prefijo de elemento recibido del formulario
    for prefix in items_prefix:
        item = Item.get(prefix)

        # Verifica si corresponde a un elemento existente en la base de datos
        if item is not None and item.list == list_obj and item.id == int(prefix):
            # Compara los datos del formulario con los datos existentes en la base de datos
            if item.name != request.POST[f'{prefix}-name'] or item.image != request.FILES.get(f'{prefix}-image'):
                item.name = request.POST[f'{prefix}-name']

                # Verifica si la imagen del elemento ha cambiado y la elimina de Cloudinary
                if item.image and request.FILES.get(f'{prefix}-image') != item.image:
                    uploader.destroy(item.image.public_id, invalidate=True)

                item.image = request.FILES.get(f'{prefix}-image')
                item.save()
        else:
            item_form = create_item_form(request, prefix=prefix)
            new_item = create_item(item_form)

            if item_form.is_valid() and new_item is not None:
                new_item.list = list_obj
                new_item.save()


def get_items(share_code, get_deleted=False):
    """Función para obtener los items de una lista"""
    # Obtenemos la lista
    list_obj = List.get(share_code)

    if list_obj is None:
        return None

    # Obtenemos los items de la lista
    if get_deleted:
        items = Item.objects.filter(list=list_obj)
    else:
        items = Item.objects.filter(list=list_obj, deleted=False)

    return items


def count_list_items(list_obj):
    """Función para contar los items de una lista"""
    return Item.objects.filter(list=list_obj, deleted=False).count()
