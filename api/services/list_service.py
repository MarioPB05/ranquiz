from api.forms.list_form import CreateListForm
from api.models import List, ListCategory
from api.services.query_service import execute_query


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


def get_lists_order_default(limit=None, page=1, search='', user=None):
    """Función que devuelve las listas públicas con filtros ordenadas por defecto"""
    query = """SELECT l.id, l.name, l.share_code, l.image,
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
                WHERE l.public = TRUE AND l.name LIKE %s
                ORDER BY 
                    CASE 
                        WHEN hl.id IS NOT NULL AND hl.start_date <= NOW() AND hl.end_date >= NOW() 
                        THEN hl.start_date 
                    END DESC
                LIMIT %s OFFSET %s;"""

    params = [user.id if user else None, f"%{search}%", limit, (page - 1) * limit]

    return execute_query(query, params)


def set_category(list_obj, category):
    """Función que añade una categoría a una lista"""
    list_category = ListCategory(list=list_obj, category=category)
    list_category.save()

    return list_category
