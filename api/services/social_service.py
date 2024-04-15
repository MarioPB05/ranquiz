from django.db.models import Sum, Case, When, Value, IntegerField, Count

from django.utils import timezone

from api.models import ListComment, CommentAward, Award
from api.services.list_service import get_list


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


def get_all_awards():
    """
    Servicio para obtener todos los premios
    """
    return Award.objects.all()


def get_awards_from_comments(comments):
    """
    Servicio para obtener todos los premios de una lista de comentarios agrupados por comentario y premio
    """
    # Obtener una lista de IDs de comentarios
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

    if selected_comment is not None and selected_user is not None:
        CommentAward.objects.create(comment=selected_comment, user=selected_user, award=selected_award)
        return True

    return False
