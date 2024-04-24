from api.forms.list_form import CreateListForm
from api.models import List, ListCategory, ListFavorite, ListLike, ListAnswer


def create_list_form(request, instance=None):
    """Obtiene el formulario para crear una lista"""
    if request.method == 'POST':
        return CreateListForm(request.POST, request.FILES, instance=instance)

    return CreateListForm(instance=instance)


def create_list(list_form):
    """Función que crea una lista"""
    if list_form.is_valid():
        return list_form.save(commit=False)

    return None


def get_list(share_code):
    """Función que devuelve el objeto "lista" al que pertenece el sharecode"""
    try:
        return List.objects.get(share_code=share_code)
    except List.DoesNotExist:
        return None


def set_category(list_obj, category):
    """Función que añade una categoría a una lista"""
    list_category = ListCategory(list=list_obj, category=category)
    list_category.save()

    return list_category


def get_list_counts(list_obj):
    """Función que devuelve la cantidad de favoritos, likes y partidas jugadas de una lista"""
    favorites_count = ListFavorite.objects.filter(list=list_obj).count()
    likes_count = ListLike.objects.filter(list=list_obj).count()
    play_count = ListAnswer.objects.filter(list=list_obj).count()

    return favorites_count, likes_count, play_count
