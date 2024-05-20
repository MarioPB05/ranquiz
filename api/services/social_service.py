from django.db.models import Count

from api.models import List, ListComment, CommentAward, Award, UserFollow, Notification
from api.models.notification_type import NotificationTypes
from api.services.query_service import execute_query


def get_comment(comment_id):
    """Función para obtener un comentario"""
    try:
        return ListComment.objects.get(id=comment_id)
    except ListComment.DoesNotExist:
        return None


def get_comments_from_list(share_code, order='featured'):
    """Servicio para obtener todos los comentarios de una lista"""
    list_element = List.get(share_code)

    if order == 'recent':
        order_by = "lc.date DESC"
    else:
        order_by = "awards DESC, lc.date DESC"

    if list_element is None:
        return None

    query = """SELECT lc.id, lc.comment, lc.date, lc.user_id, au.username, aa.image as avatar, au.share_code,
                    (SELECT SUM(a.price) FROM api_commentaward ca
                    JOIN ranquiz.api_award a on a.id = ca.award_id
                    WHERE ca.comment_id = lc.id) as awards
                FROM api_listcomment lc
                JOIN ranquiz.api_user au on lc.user_id = au.id
                JOIN ranquiz.api_avatar aa on au.avatar_id = aa.id
                WHERE lc.list_id = %s
                ORDER BY %s;"""  # skipcq: BAN-B608

    params = [list_element.id, order_by]

    return execute_query(query, params)


def create_comment(content, author, share_code):
    """Servicio para crear un comentario"""
    list_element = List.get(share_code)

    if list_element is not None and content is not None and author is not None:
        comment = ListComment.objects.create(list=list_element, user=author, comment=content)
        Notification.create(1, NotificationTypes.NEW_LIST_COMMENT.object, list_element.owner,
                            list_element.share_code)
        return comment

    return None


def get_all_awards():
    """Servicio para obtener todos los premios"""
    return Award.objects.all()


def get_awards_from_comments(comments, dictionary=False):
    """Servicio para obtener todos los premios de una lista de comentarios agrupados por comentario y premio"""
    # Obtener una lista de IDs de comentarios
    comment_ids = []

    if dictionary:
        comment_ids = [comment['id'] for comment in comments]
    else:
        comment_ids = [comment.id for comment in comments]

    # Realizar una consulta para obtener los premios agrupados por ID de comentario y premio, y contar la cantidad
    awards_queryset = CommentAward.objects.filter(comment_id__in=comment_ids).values('comment_id', 'award_id').annotate(
        amount=Count('award_id'))

    # Crear un diccionario para almacenar los premios agrupados por comentario
    awards_dict = {}

    # Iterar sobre los resultados de la consulta
    for award_data in awards_queryset:
        # Obtener el ID del comentario y del premio
        comment_id = award_data['comment_id']
        award_id = award_data['award_id']
        amount = award_data['amount']

        # Si el ID del comentario ya está en el diccionario, agregar el premio a la lista existente
        if comment_id in awards_dict:
            awards_dict[comment_id].append({'id_award': award_id, 'amount': amount})
        # Si el ID del comentario no está en el diccionario, crearlo con una lista que contenga el premio
        else:
            awards_dict[comment_id] = [{'id_award': award_id, 'amount': amount}]

    return awards_dict


def get_award(award_id):
    """Servicio para obtener un premio"""
    try:
        return Award.objects.get(id=award_id)
    except Award.DoesNotExist:
        return None


def check_user_award_in_comment(comment_id, user_id, award_id):
    """Servicio para comprobar si un usuario ya ha otorgado un premio al comentario"""
    selected_comment = get_comment(comment_id)
    selected_user = user_id
    selected_award = get_award(award_id)

    if selected_comment is not None and selected_user is not None and selected_award is not None:
        return CommentAward.objects.filter(comment=selected_comment, user=selected_user, award=selected_award).exists()

    return False


def add_award_to_comment(comment_id, selected_user, award_id):
    """Servicio para añadir un premio a un comentario"""
    selected_comment = get_comment(comment_id)
    selected_award = get_award(award_id)

    if selected_comment is not None and selected_user is not None:
        CommentAward.objects.create(comment=selected_comment, user=selected_user, award=selected_award)
        Notification.create(1, NotificationTypes.NEW_COMMENT_AWARD.object, selected_comment.user,
                            selected_comment.list.share_code)
        return True

    return False


def get_followers(user):
    """Obtiene los seguidores de un usuario"""
    return UserFollow.objects.filter(user_followed=user)


def get_following(user):
    """Obtiene los usuarios que sigue un usuario"""
    return UserFollow.objects.filter(follower=user)
