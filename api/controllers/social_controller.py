from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from api.decorators.api_decorators import require_authenticated
from api.services.social_service import (get_comments_from_list, create_comment, get_awards_from_comments, get_comment,
                                         get_award, add_award_to_comment, check_user_award_in_comment, get_all_awards)
from api.services.transaction_service import do_transaction


@require_GET
def get_comments(request, share_code):
    """Función para obtener todos los comentarios de una lista"""
    mode = request.GET.get('mode')  # featured, recent
    comments = get_comments_from_list(share_code, mode)

    if comments is None:
        return JsonResponse({'status': 'error', 'message': 'Lista no encontrada'})

    json_comments = []
    comments_award = get_awards_from_comments(comments, True)

    for comment in comments:
        awards_in_comment = None

        if comment['awards'] != "0":
            awards_in_comment = comments_award.get(comment['id'])

        json_comments.append({
            'id': comment['id'],
            'content': comment['comment'],
            'date': comment['date'],
            'user_is_author': comment['user_id'] == request.user.id,
            'author': {
                'name': comment['username'],
                'avatar': f"https://res.cloudinary.com/dhewpzvg9/{comment['avatar']}",
                'url': request.build_absolute_uri(reverse('user', args=[comment['share_code']]))
            },
            'awards': awards_in_comment if awards_in_comment is not None else [],
        })

    return JsonResponse({'comments': json_comments})


@require_POST
@require_authenticated
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


def get_awards(request):
    """Función para obtener todos los premios"""
    awards = get_all_awards()

    json_awards = []

    for award in awards:
        json_awards.append({
            'id': award.id,
            'icon': award.icon,
            'title': award.title,
            'color': award.color,
            'price': award.price,
        })

    return JsonResponse({'awards': json_awards})


@require_GET
@require_authenticated
def add_award_to_comment_function(request, share_code, comment_id):  # skipcq: PYL-W0613
    """Función para añadir un premio a un comentario"""
    award_id = request.POST.get('id_award')
    selected_comment = get_comment(comment_id)
    selected_award = get_award(award_id)
    final_price = int(selected_award.price * 0.7)

    # Verificar si el usuario ya otorgó este premio en este comentario
    if check_user_award_in_comment(comment_id, request.user, award_id):
        return JsonResponse({'status': 'Error', 'message': 'Ya has otorgado este premio en este comentario'})

    # Verificar si el usuario está intentando otorgar un premio a su propio comentario
    if request.user.id == selected_comment.user.id:
        return JsonResponse({'status': 'Error', 'message': 'No puedes otorgar un premio a tu propio comentario'})

    # Realizar la transacción para pagar el premio
    transaction_paid = do_transaction(request.user, -selected_award.price, "Premio otorgado")
    if transaction_paid is None:
        return JsonResponse({'status': 'Error', 'message': 'No tienes suficientes puntos para otorgar este premio'})

    # Realizar la transacción para recibir el premio
    transaction_received = do_transaction(selected_comment.user, final_price, "Premio recibido")
    if transaction_received is None:
        # Reembolsar al usuario si hay un error al recibir el premio
        do_transaction(request.user, selected_award.price, "Premio reembolsado por error al otorgar el premio")
        return JsonResponse({'status': 'Error', 'message': 'Error al otorgar el premio'})

    try:
        # Intentar agregar el premio al comentario
        if add_award_to_comment(comment_id, request.user, award_id):
            return JsonResponse({'status': 'Success', 'message': 'Premio otorgado'})

    except Exception:
        # Reembolsar a los usuarios si hay un error al agregar el premio al comentario
        do_transaction(request.user, selected_award.price, "Premio reembolsado por error al otorgar el premio")
        do_transaction(selected_comment.user, -final_price, "Premio reembolsado por error al otorgar el premio")

    return JsonResponse({'status': 'Error', 'message': 'Error al otorgar el premio'})
