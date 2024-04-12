from django.db.models import Sum
from django.utils import timezone

from api.models import ListComment, CommentAward, User
from api.services.list_service import get_list


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
        return ListComment.objects.annotate(award_prices=Sum("commentaward__award__price")).order_by('-award_prices')

    return None


def get_featured_comments_from_list(share_code, user):
    """Servicio para obtener los comentarios destacados de una lista"""
    list_element = get_list(share_code)
    selected_user = user

    # Filtrar los comentarios por el usuario y ordenarlos por el número de premios
    comentarios_usuario = ListComment.objects.filter(list=list_element, user=selected_user).annotate(
        award_prices=Sum('commentaward__award__price')).order_by('-award_prices')

    # Filtrar los comentarios que no son del usuario y ordenarlos por el número de premios
    otros_comentarios = ListComment.objects.filter(list=list_element).exclude(user=selected_user).annotate(
        award_prices=Sum('commentaward__award__price')).order_by('-award_prices')

    # Unir los dos conjuntos de comentarios
    return otros_comentarios.union(comentarios_usuario)


def create_comment(content, author, share_code):
    """Servicio para crear un comentario"""
    list_element = get_list(share_code)

    if list_element is not None and content is not None and author is not None:
        current_datetime = timezone.now()
        return ListComment.objects.create(list=list_element, user=author, comment=content, date=current_datetime)

    return None

