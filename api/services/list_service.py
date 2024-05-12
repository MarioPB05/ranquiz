import math

from django.db.models import Q

from django.db import transaction

from api.forms.list_form import CreateListForm
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.query_service import execute_query
from api.models import ListCategory, ListFavorite, ListLike, ListAnswer, ItemOrder, ListComment, List, Item


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


def get_lists(limit=None, page=1, search='', user=None, order='default', category=None):
    """Función que devuelve las listas públicas con filtros"""
    order_by = ""
    where = ""

    if order == 'popular':
        order_by = "plays DESC, "
    elif order == 'newest':
        order_by = "l.edit_date DESC, "

    order_by += ("CASE WHEN "
                 "hl.id IS NOT NULL THEN hl.start_date ELSE l.creation_date END DESC")

    if category is not None:
        where = "AND lc.category_id = %s "

    query = """SELECT l.id, l.name, l.share_code, l.image,
                    (SELECT IF(COUNT(sll.id) > 0, TRUE, FALSE)
                     FROM api_listlike sll
                     WHERE sll.list_id = l.id AND sll.user_id = %s) AS liked,
                    (SELECT COUNT(sla.id)
                     FROM api_listanswer sla
                     WHERE sla.list_id = l.id) AS plays,
                    IF(hl.id IS NOT NULL, TRUE, FALSE)
                    AS highlighted,
                    au.username as owner_username, au.share_code as owner_share_code, aa.image as owner_avatar
                FROM api_list l
                JOIN ranquiz.api_user au on l.owner_id = au.id
                JOIN ranquiz.api_avatar aa on au.avatar_id = aa.id
                LEFT JOIN ranquiz.api_highlightedlist hl on l.id = hl.list_id AND start_date <= NOW() 
                    AND end_date >= NOW()
                LEFT JOIN ranquiz.api_listcategory lc on l.id = lc.list_id
                WHERE l.public = TRUE AND l.name LIKE %s %s
                GROUP BY l.id
                ORDER BY %s
                LIMIT %s OFFSET %s;"""

    params = [user.id if user is not None else 0, f"%{search}%", where, order_by, limit, (page - 1) * limit]

    if category is not None:
        params.insert(2, category.id)

    return execute_query(query, params)


def get_user_lists(user, show_deleted, visibility, search_query, page_number):
    """Función que devuelve todas las listas de un usuario con paginación"""
    where_conditions = ["l.owner_id = %s"]
    params = [user.id]

    if not show_deleted:
        where_conditions.append("l.deleted = 0")

    if search_query:
        where_conditions.append("l.name LIKE %s")
        search_query = f'%{search_query}%'
        params.append(search_query)

    if visibility == 'public':
        where_conditions.append("l.public = 1")
    elif visibility == 'private':
        where_conditions.append("l.public = 0")

    where_clause = " AND ".join(where_conditions)

    query = f"""SELECT l.id, l.name, l.share_code, l.image, l.public, l.edit_date, l.creation_date, l.deleted,
                    (
                        SELECT COUNT(*)
                        FROM api_listlike sll
                        WHERE sll.list_id = l.id
                    ) AS likes,
                    (
                        SELECT COUNT(*)
                        FROM api_listfavorite slf
                        WHERE slf.list_id = l.id
                    ) AS favorites,
                    (
                        SELECT COUNT(*)
                        FROM api_listanswer sla
                        WHERE sla.list_id = l.id
                    ) AS plays,
                    (
                        SELECT COUNT(*)
                        FROM api_listcomment slc
                        WHERE slc.list_id = l.id
                    ) AS comments,
                    IF(hl.id IS NOT NULL, TRUE, FALSE)
                    AS highlighted, au.share_code as owner_share_code, aa.image as owner_avatar, 
                    au.username as owner_username
                FROM api_list l
                JOIN ranquiz.api_user au on l.owner_id = au.id
                JOIN ranquiz.api_avatar aa on au.avatar_id = aa.id
                LEFT JOIN ranquiz.api_highlightedlist hl on l.id = hl.list_id AND start_date <= NOW() 
                    AND end_date >= NOW()
                LEFT JOIN ranquiz.api_listcategory lc on l.id = lc.list_id
                WHERE {where_clause}
                GROUP BY l.id, l.edit_date, l.creation_date
                ORDER BY l.edit_date DESC, l.creation_date DESC
                LIMIT %s OFFSET %s;"""

    items_per_page = PAGINATION_ITEMS_PER_PAGE / 2
    params.extend([int(items_per_page), int((page_number - 1) * items_per_page)])

    return execute_query(query, params)


def get_user_lists_pagination(user, show_deleted, visibility, search_query, page_number):
    """Función que devuelve la cantidad de listas de un usuario"""
    query = Q(owner=user)

    if not show_deleted:
        query &= Q(deleted=False)

    if visibility == 'public':
        query &= Q(public=True)
    elif visibility == 'private':
        query &= Q(public=False)

    if search_query:
        query &= Q(name__icontains=search_query)

    count = List.objects.filter(query).count()

    pages = math.ceil(count / (PAGINATION_ITEMS_PER_PAGE / 2))

    return {
        'total': count,
        'pages': pages,
        'number': page_number,
        'page_range': [i for i in range(1, int(pages) + 1)],
        'has_previous': page_number > 1,
        'has_next': page_number < pages,
        'has_other_pages': pages > 1,
        'previous_page_number': page_number - 1,
        'next_page_number': page_number + 1,
    }


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
    comments_count = ListComment.objects.filter(list=list_obj).count()

    return favorites_count, likes_count, play_count, comments_count


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


def toggle_visibility_list(share_code):
    """Función que cambia la visibilidad de una lista"""
    list_obj = List.get(share_code)
    list_obj.public = not list_obj.public
    list_obj.save()


def delete_list(share_code):
    """Función que elimina una lista"""
    list_obj = List.get(share_code)

    if list_obj is None:
        return False

    list_obj.deleted = True
    list_obj.public = False
    list_obj.save()

    return True


def recover_list(share_code):
    """Función que recupera una lista"""
    list_obj = List.get(share_code)

    if list_obj is None:
        return False

    list_obj.deleted = False
    list_obj.save()

    return True


def toggle_like_list(user, share_code):
    """Función que permite dar like o quitar el like a una lista"""
    list_obj = List.get(share_code)

    if list_obj is None:
        return False

    try:
        like = ListLike.objects.get(user=user, list=list_obj)
        like.delete()
    except ListLike.DoesNotExist:
        like = ListLike(user=user, list=list_obj)
        like.save()

    return True


def toggle_favorite_list(user, share_code):
    """Función que permite añadir o quitar una lista de favoritos"""
    list_obj = List.get(share_code)

    if list_obj is None:
        return False

    try:
        favorite = ListFavorite.objects.get(user=user, list=list_obj)
        favorite.delete()
    except ListFavorite.DoesNotExist:
        favorite = ListFavorite(user=user, list=list_obj)
        favorite.save()

    return True


@transaction.atomic
def add_result(user, list_obj, results, start_date):
    """Servicio que añade un resultado a una lista con una transacción"""
    list_answer = ListAnswer(user=user, list=list_obj, start_date=start_date)
    list_answer.save()

    for result in results:
        item = Item.get(result['id'])
        order = int(result['order'])

        if item is not None:
            item_order = ItemOrder(answer=list_answer, item=item, order=order)
            item_order.save()

    return list_answer
