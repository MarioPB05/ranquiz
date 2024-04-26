from api.forms.category_form import CreateCategoryForm
from api.models import Category
from api.services.list_service import set_category
from api.services.query_service import execute_query


def create_category(data):
    """Función para crear una categoría"""
    category_form = CreateCategoryForm(data)

    if category_form.is_valid():
        # Guardamos la categoría y la devolvemos
        return category_form.save()

    return None


def edit_list_categories(categories_names, list_obj):
    """Función para editar las categorías de una lista"""
    # Elimina las categorías existentes de la lista antes de añadir las nuevas
    list_obj.listcategory_set.all().delete()
    if categories_names is not None:
        for category_name in categories_names:
            category = get_category(category_name=category_name)

            if category is not None:
                set_category(list_obj, category)


def get_category(category_id=None, category_name=None, share_code=None):
    """Función para obtener una categoría"""
    if category_id is not None:
        return Category.objects.get(id=category_id)

    if category_name is not None:
        return Category.objects.get(name=category_name)

    if share_code is not None:
        return Category.objects.get(share_code=share_code)

    return None


def get_all_categories():
    """Función para obtener todas las categorías"""
    # Obtenemos todas las categorías
    categories = Category.objects.all()

    return categories


def get_categories(limit=None, page=1, search='', user=None, order='default'):
    """Función para obtener todas las categorías"""
    order_by = "1"

    if order == 'default':
        order_by = "id DESC"
    elif order == 'popular':
        order_by = "followers DESC"
    elif order == 'newest':
        order_by = "max(al.edit_date) DESC"

    query = """SELECT c.id, c.name, c.share_code, COUNT(lc.list_id) as lists, COUNT(cs.user_id) as followers,
                if(cs.user_id = %s, TRUE, FALSE) as followed
                FROM api_category c
                LEFT JOIN api_listcategory lc on c.id = lc.category_id
                LEFT JOIN api_categorysubscription cs on c.id = cs.category_id
                JOIN ranquiz.api_list al on lc.list_id = al.id
                WHERE c.name LIKE %s
                GROUP BY c.id
                ORDER BY %s
                LIMIT %s OFFSET %s;"""

    params = [user.id if user is not None else 0, f"%{search}%", order_by, limit, (page - 1) * limit]

    return execute_query(query, params)


def edit_distance(s1, s2):
    """Función para calcular la distancia de edición entre dos cadenas"""
    s1 = s1.lower()
    s2 = s2.lower()

    costs = [0] * (len(s2) + 1)
    for i in range(len(s1) + 1):
        last_value = i
        for j in range(len(s2) + 1):
            if i == 0:
                costs[j] = j
            else:
                if j > 0:
                    new_value = costs[j - 1]
                    if s1[i - 1] != s2[j - 1]:
                        new_value = min(min(new_value, last_value), costs[j]) + 1
                    costs[j - 1] = last_value
                    last_value = new_value
        if i > 0:
            costs[len(s2)] = last_value
    return costs[len(s2)]


def similarity(s1, s2):
    """Función para calcular la similitud entre dos cadenas"""
    longer = s1
    shorter = s2
    if len(s1) < len(s2):
        longer = s2
        shorter = s1
    longer_length = len(longer)
    if longer_length == 0:
        return 1.0
    return (longer_length - edit_distance(longer, shorter)) / float(longer_length)


def user_followed_category(user, category):
    """Función para comprobar si un usuario sigue una categoría"""
    return user.categorysubscription_set.filter(category=category).exists()
