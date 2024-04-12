from cloudinary import CloudinaryImage
from django.http import JsonResponse

from api.services.social_service import get_comments_from_list, create_comment, get_featured_comments_from_list, \
    get_most_awarded_comments_from_list, get_awards_from_comment, get_comment, get_award, add_award_to_comment


def get_comments(request, share_code):
    """Función para obtener todos los comentarios de una lista"""
    comments = []
    mode = request.GET.get('mode')

    if mode == 'most_awarded':
        comments = get_most_awarded_comments_from_list(share_code)

    elif mode == 'featured':
        comments = get_featured_comments_from_list(share_code, request.user)

    elif mode == 'recient':
        comments = get_comments_from_list(share_code)

    json_comments = []

    for comment in comments:

        json_comments.append({
            'id': comment.id,
            'content': comment.comment,
            'date': comment.date,
            'author': {
                'name': comment.user.username,
                'avatar': f"https://res.cloudinary.com/dhewpzvg9/{comment.user.avatar.image}",
            },
            'awards': get_awards_from_comment(comment.id),
        })

    return JsonResponse({'comments': json_comments})


def create_and_return_comment(request, share_code):
    """Función para crear un comentario"""
    content = request.POST.get('content')
    author = request.user

    if author is not None:
        comment = create_comment(content, author, share_code)

        return JsonResponse({"comment": {
            'id': comment.id,
            'content': comment.comment,
            'date': comment.date,
            'author': {
                'name': comment.user.username,
                'avatar': f"https://res.cloudinary.com/dhewpzvg9/{comment.user.avatar.image}"
            },
        }})

    return None


def add_award_to_comment_function(request, share_code, comment_id):
    """Función para añadir un premio a un comentario"""
    award_id = request.POST.get('id_award')

    if add_award_to_comment(comment_id, request.user, award_id):
        return JsonResponse({'status': 'Success', 'message': 'Premio otorgado'})

    return JsonResponse({'status': 'Error', 'message': 'Error al otorgar el premio'})
