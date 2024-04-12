from django.http import JsonResponse

from api.services.social_service import get_comments_from_list, create_comment, get_featured_comments_from_list


def get_comments(request, share_code):
    """Función para obtener todos los comentarios de una lista"""
    comments = get_featured_comments_from_list(share_code, request.user)
    json_comments = []

    for comment in comments:

        json_comments.append({
            'id': comment.id,
            'content': comment.comment,
            'date': comment.date,
            'author': {
                'name': comment.user.username,
                # 'avatar': comment.user.avatar.image
            },
            'awards': [
                {
                    'id': award.id,
                    'title': award.title,
                    'icon': award.icon,
                } for award in comment.commentaward_set.all()
            ]
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
                # 'avatar': comment.user.avatar.image
            },
        }})

    return None
