from cloudinary import CloudinaryImage
from django.http import JsonResponse

from api.services.social_service import get_comments_from_list, create_comment, get_featured_comments_from_list, \
    get_most_awarded_comments_from_list, get_awards_from_comment, get_comment, get_award, add_award_to_comment, \
    check_user_award_in_comment
from api.services.transaction_service import do_transaction


def get_comments(request, share_code):
    """Función para obtener todos los comentarios de una lista"""
    comments = []
    mode = request.GET.get('mode')

    if mode == 'most_awarded':
        comments = get_most_awarded_comments_from_list(share_code)

    elif mode == 'featured':
        if request.user.is_authenticated:
            comments = get_featured_comments_from_list(share_code, request.user)
        else:
            comments = get_most_awarded_comments_from_list(share_code)

    elif mode == 'recient':
        comments = get_comments_from_list(share_code)

    json_comments = []

    for comment in comments:

        json_comments.append({
            'id': comment.id,
            'content': comment.comment,
            'date': comment.date,
            'user_is_author': comment.user.id == request.user.id,
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
            'user_is_author': comment.user.id == request.user.id,
            'author': {
                'name': comment.user.username,
                'avatar': f"https://res.cloudinary.com/dhewpzvg9/{comment.user.avatar.image}"
            },
        }})

    return None


def add_award_to_comment_function(request, share_code, comment_id):
    """Función para añadir un premio a un comentario"""
    award_id = request.POST.get('id_award')
    selected_comment = get_comment(comment_id)
    selected_award = get_award(award_id)

    if check_user_award_in_comment(comment_id, request.user, award_id):
        return JsonResponse({'status': 'Error', 'message': 'Ya has otorgado este premio en este comentario'})

    if request.user.id == selected_comment.user.id:
        return JsonResponse({'status': 'Error', 'message': 'No puedes otorgar un premio a tu propio comentario'})

    transaction_paid = do_transaction(request.user, -selected_award.price, "Premio otorgado")

    if transaction_paid is None:
        return JsonResponse({'status': 'Error', 'message': 'No tienes suficientes puntos para otorgar este premio'})

    transaction_received = do_transaction(selected_comment.user, selected_award.price, "Premio recibido")

    if transaction_received is None:
        do_transaction(request.user, selected_award.price, "Premio reembolsado por error al otorgar el premio")
        return JsonResponse({'status': 'Error', 'message': 'Error al otorgar el premio'})
    try:
        if add_award_to_comment(comment_id, request.user, award_id):
            return JsonResponse({'status': 'Success', 'message': 'Premio otorgado'})

    except Exception as e:
        do_transaction(request.user, selected_award.price, "Premio reembolsado por error al otorgar el premio")
        do_transaction(selected_comment.user, -selected_award.price,"Premio reembolsado por error al otorgar el premio")

    return JsonResponse({'status': 'Error', 'message': 'Error al otorgar el premio'})
