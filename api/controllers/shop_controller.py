from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.services import shop_service
from api.services.shop_service import calculate_highlight_price, get_all_avatars, get_avatars_by_popularity, \
    get_avatars_by_purchased, buy_avatar, equip_avatar
from api.services.transaction_service import do_transaction, refund_transaction


@require_GET
def highlight_calculator(request):
    """Controlador que devuelve el precio de destacar una lista"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_price = calculate_highlight_price(start_date, end_date)

    return JsonResponse({'price': total_price})


@require_GET
def list_is_highlighted(request, share_code):
    """Controlador que comprueba si una lista está destacada"""
    result = shop_service.list_is_highlighted(share_code)
    return JsonResponse({'highlighted': result})


@require_GET
@require_authenticated
def highlight_list(request, share_code):
    """Controlador que permite destacar una lista"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if share_code is None or start_date is None or end_date is None:
        return JsonResponse({'status': 'error', 'message': 'Comprueba que la lista sea pública'})

    value = calculate_highlight_price(start_date, end_date)

    if value <= 0:
        return JsonResponse({'status': 'error', 'message': 'El precio de destacar la lista es incorrecto'})

    transaction_paid = do_transaction(request.user, -value, "Destacar lista")

    if transaction_paid is None:
        return JsonResponse({'status': 'error', 'message': 'No tienes suficientes diamantes para destacar la lista'})

    result = shop_service.highlight_list(share_code, start_date, end_date, transaction_paid)

    if result is not None:
        return JsonResponse({'status': 'success', 'message': 'La lista ha sido destacada'})

    refund_transaction(transaction_paid)

    return JsonResponse({'status': 'error', 'message': 'Error al destacar la lista'})


@require_GET
def get_avatars(request):
    """Controlador que devuelve todos los avatares"""
    mode = request.GET.get('mode')
    avatars = None
    result = []

    if mode == 'rarity':
        avatars = get_all_avatars(request.user)
    elif mode == 'popular':
        avatars = get_avatars_by_popularity(request.user)
    elif mode == 'purchased':
        avatars = get_avatars_by_purchased(request.user)

    for avatar in avatars:
        result.append({
            'id': avatar.id,
            'name': avatar.title,
            'rarity': avatar.rarity.name,
            'price': avatar.rarity.price,
            'image': f"https://res.cloudinary.com/dhewpzvg9/{avatar.image}",
            'bought': avatar.rarity.id == 1 or avatar.is_user_avatar,
            'equipped': request.user.avatar.id == avatar.id,
        })

    return JsonResponse({'avatars': result})


@require_GET
@require_authenticated
def buy_a_avatar(request, avatar_id):
    """Controlador que compra un avatar"""
    user = request.user

    if buy_avatar(user, avatar_id) is None:
        return JsonResponse({'status': 'error', 'message': 'Ha ocurrido un error al comprar el avatar'})

    return JsonResponse({'status': 'success', 'message': 'El avatar ha sido comprado'})


@require_GET
@require_authenticated
def equip_a_avatar(request, avatar_id):
    """Controlador que equipa un avatar"""
    user = request.user

    if equip_avatar(user, avatar_id) is None:
        return JsonResponse({'status': 'error', 'message': 'Ha ocurrido un error al equipar el avatar'})

    return JsonResponse({'status': 'success', 'message': 'El avatar ha sido equipado'})
