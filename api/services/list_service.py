from api.forms.list_form import CreateListForm
from api.services.query_service import execute_query
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
    """Función que devuelve el objeto "lista" al que pertenece el share code"""
    try:
        return List.objects.get(share_code=share_code)
    except List.DoesNotExist:
        return None


def get_lists(limit=None, page=1, search='', user=None, order='default', category=None):
    """Función que devuelve las listas públicas con filtros"""
    order_by = ""
    where = ""

    if order == 'popular':
        order_by = "plays DESC, "
    elif order == 'newest':
        order_by = "l.edit_date DESC, "

    order_by += ("CASE "
                 "WHEN hl.id IS NOT NULL AND hl.start_date <= NOW() AND hl.end_date >= NOW() "
                 "THEN hl.start_date END DESC")

    if category is not None:
        where = "AND lc.category_id = %s "

    query = f"""SELECT l.id, l.name, l.share_code, l.image,
                    (SELECT IF(COUNT(sll.id) > 0, TRUE, FALSE)
                     FROM api_listlike sll
                     WHERE sll.list_id = l.id AND sll.user_id = %s) AS liked,
                    (SELECT COUNT(sla.id)
                     FROM api_listanswer sla
                     WHERE sla.list_id = l.id) AS plays,
                    IF(hl.id IS NOT NULL AND hl.start_date <= NOW() AND hl.end_date >= NOW(), TRUE, FALSE)
                    AS highlighted,
                    au.username as owner_username, au.share_code as owner_share_code, aa.image as owner_avatar
                FROM api_list l
                JOIN ranquiz.api_user au on l.owner_id = au.id
                JOIN ranquiz.api_avatar aa on au.avatar_id = aa.id
                LEFT JOIN ranquiz.api_highlightedlist hl on l.id = hl.list_id
                LEFT JOIN ranquiz.api_listcategory lc on l.id = lc.list_id
                WHERE l.public = TRUE AND l.name LIKE %s {where}
                GROUP BY l.id
                ORDER BY {order_by}
                LIMIT %s OFFSET %s;"""

    params = [user.id if user is not None else 0, f"%{search}%", limit, (page - 1) * limit]

    if category is not None:
        params.insert(2, category.id)

    return execute_query(query, params)


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


def count_lists(search='', category=None):
    """Función que devuelve la cantidad de listas públicas con filtros"""
    where = ""

    if category is not None:
        where = "AND lc.category_id = %s "

    query = f"""SELECT COUNT(l.id) as count
                FROM api_list l
                JOIN ranquiz.api_user au on l.owner_id = au.id
                JOIN ranquiz.api_avatar aa on au.avatar_id = aa.id
                LEFT JOIN ranquiz.api_listcategory lc on l.id = lc.list_id
                WHERE l.public = TRUE AND l.name LIKE %s {where};"""

    params = [f"%{search}%"]

    if category is not None:
        params.insert(1, category.id)

    return execute_query(query, params)
