from django.db.models import Sum, F, Case, When, Value, IntegerField

from django.utils import timezone

from api.models import ListComment, CommentAward, Award
from api.services.list_service import get_list
from api.services.transaction_service import do_transaction


def get_comment(comment_id):
    """Función para obtener un comentario"""
    try:
        return ListComment.objects.get(id=comment_id)
    except ListComment.DoesNotExist:
        return None


def get_comments_from_list(share_code):
    """Servicio para obtener todos los comentarios de una lista"""
    list_element = get_list(share_code)

    if list_element is not None:
        return ListComment.objects.filter(list=list_element)

    return None


def get_most_awarded_comments_from_list(share_code):
    """Servicio para obtener todos los comentarios de una lista ordenados por la cantidad de premios que han recibido"""
    list_element = get_list(share_code)

    if list_element is not None:
        return ListComment.objects.annotate(award_prices=Sum("commentaward__award__price")).order_by('award_prices')

    return None


def get_featured_comments_from_list(share_code, user):
    """Servicio para obtener los comentarios destacados de una lista"""
    list_element = get_list(share_code)
    selected_user = user

    # Anotar los comentarios con el número de premios
    comentarios_anotados = ListComment.objects.filter(list=list_element).annotate(
        award_prices=Sum('commentaward__award__price'),
        is_selected_user=Case(
            When(user=selected_user, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    )

    # Ordenar los comentarios por el número de premios y si pertenecen al usuario seleccionado
    comentarios_ordenados = comentarios_anotados.order_by('is_selected_user', 'award_prices')

    return comentarios_ordenados


def create_comment(content, author, share_code):
    """Servicio para crear un comentario"""
    list_element = get_list(share_code)

    if list_element is not None and content is not None and author is not None:
        current_datetime = timezone.now()
        return ListComment.objects.create(list=list_element, user=author, comment=content, date=current_datetime)

    return None


def get_awards_from_comment(comment_id):
    """
    Servicio para obtener todos los premios de un comentario agrupados
    """
    selected_comment = get_comment(comment_id)

    if selected_comment is not None:
        awards_dict = {}
        for award in selected_comment.commentaward_set.all():
            award_id = award.award.id
            if award_id in awards_dict:
                awards_dict[award_id]['amount'] += 1
            else:
                awards_dict[award_id] = {
                    'id_award': award_id,
                    'amount': 1
                }

        return list(awards_dict.values())

    return None


def get_award(award_id):
    """
    Servicio para obtener un premio
    """
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
    """
    Servicio para añadir un premio a un comentario
    """
    selected_comment = get_comment(comment_id)
    selected_award = get_award(award_id)
    comment_user = selected_comment.user

    if (do_transaction(selected_user, -selected_award.price, "Premio otorgado") is None or
            do_transaction(comment_user, selected_award.price, "Premio recibido") is None):
        # TODO: Devolver dinero al usuario si se produce un error
        return False

    if selected_comment is not None and selected_user is not None:
        CommentAward.objects.create(comment=selected_comment, user=selected_user, award=selected_award)
        return True

    return False
