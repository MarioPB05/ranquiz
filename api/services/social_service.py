from django.utils import timezone

from api.models import ListComment
from api.services.list_service import get_list


def get_comments_from_list(share_code):
    """Servicio para obtener todos los comentarios de una lista"""
    list_element = get_list(share_code)

    if list_element is not None:
        return ListComment.objects.filter(list=list_element)

    return None


def create_comment(content, author, share_code):
    """Servicio para crear un comentario"""
    list_element = get_list(share_code)

    if list_element is not None and content is not None and author is not None:
        current_datetime = timezone.now()
        return ListComment.objects.create(list=list_element, user=author, comment=content, date=current_datetime)

    return None

