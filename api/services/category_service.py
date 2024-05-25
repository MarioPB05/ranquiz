from api.forms.category_form import CreateCategoryForm
from api.models import Category
from api.services import PAGINATION_ITEMS_PER_PAGE
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
    try:
        if category_id is not None:
            return Category.objects.get(id=category_id)

        if category_name is not None:
            return Category.objects.get(name=category_name)

        if share_code is not None:
            return Category.objects.get(share_code=share_code)

        return None
    except Category.DoesNotExist:
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
        order_by = "lists DESC"
    elif order == 'popular':
        order_by = "followers DESC"
    elif order == 'newest':
        order_by = "c.id DESC"

    query = f"""SELECT c.*,
                (
                    SELECT COUNT(scs.id)
                    FROM api_categorysubscription scs
                    WHERE scs.category_id = c.id
                ) as followers,
                (
                    SELECT COUNT(slc.id)
                    FROM api_listcategory slc
                    JOIN api_list sal on slc.list_id = sal.id
                    WHERE slc.category_id = c.id AND sal.public = TRUE
                ) as lists,
                (
                    SELECT IF(COUNT(scs.id) > 0, TRUE, FALSE)
                    FROM api_categorysubscription scs
                    WHERE scs.category_id = c.id AND scs.user_id = %s
                ) as followed
                FROM api_category c
                WHERE c.name LIKE %s and (
                    SELECT COUNT(slc.id)
                    FROM api_listcategory slc
                    JOIN api_list sal on slc.list_id = sal.id
                    WHERE slc.category_id = c.id AND sal.public = TRUE
                ) > 0
                ORDER BY {order_by}
                LIMIT %s OFFSET %s;"""

    params = [user.id if user.id is not None else 0, f"%{search}%", limit, (page - 1) * limit]

    return execute_query(query, params)


def get_user_categories(profile_user, current_user, page=1):
    """Función para obtener todas las categorías de un usuario"""
    query = """SELECT c.*,
                (
                    SELECT COUNT(scs.id)
                    FROM api_categorysubscription scs
                    WHERE scs.category_id = c.id
                ) as followers,
                (
                    SELECT COUNT(slc.id)
                    FROM api_listcategory slc
                    JOIN api_list sal on slc.list_id = sal.id
                    WHERE slc.category_id = c.id AND sal.public = TRUE
                ) as lists,
                (
                    SELECT IF(COUNT(scs.id) > 0, TRUE, FALSE)
                    FROM api_categorysubscription scs
                    WHERE scs.category_id = c.id AND scs.user_id = %s
                ) as followed
                FROM api_category c
                LEFT JOIN ranquiz.api_categorysubscription ac on c.id = ac.category_id
                WHERE ac.user_id = %s
                LIMIT %s OFFSET %s;"""

    params = [current_user.id, profile_user.id, PAGINATION_ITEMS_PER_PAGE, (page - 1) * PAGINATION_ITEMS_PER_PAGE]

    print(params)

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


def user_follow_category(user, category, follow=False, notification=False):
    """Función para que un usuario siga o des siga una categoría"""
    if user.is_authenticated and category is not None:
        # Comprobamos si el usuario ya sigue la categoría
        if user.categorysubscription_set.filter(category=category).exists():
            # Si no queremos seguir la categoría, la eliminamos
            if not follow:
                user.categorysubscription_set.filter(category=category).delete()
                return True

            # Si queremos seguir la categoría, actualizamos la notificación
            user.categorysubscription_set.filter(category=category).update(notification=notification)
            return True

        # Creamos la suscripción
        if follow:
            user.categorysubscription_set.create(category=category, notification=notification)

        return True

    return False


def user_followed_category(user, category):
    """Función para comprobar si un usuario sigue una categoría"""
    if user.is_authenticated and category is not None:
        return user.categorysubscription_set.filter(category=category).exists()

    return False


def user_follow_category_and_receive_notifications(user, category):
    """Función para comprobar si un usuario sigue una categoría y recibe notificaciones"""
    if user.is_authenticated and category is not None:
        return user.categorysubscription_set.filter(category=category, notification=True).exists()

    return False
