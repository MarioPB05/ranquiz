from django.http import JsonResponse

from api.services.shop_service import calculate_highlight_price, get_all_avatars, get_avatars_by_popularity, \
    get_avatars_by_purchased, buy_avatar, equip_avatar


def highlight_calculator(request):
    """Controlador que devuelve el precio de destacar una lista"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_price = calculate_highlight_price(start_date, end_date)

    return JsonResponse({'price': total_price})


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


def buy_a_avatar(request, avatar_id):
    """Controlador que compra un avatar"""
    user = request.user

    if buy_avatar(user, avatar_id) is None:
        return JsonResponse({'status': 'error', 'message': 'Ha ocurrido un error al comprar el avatar'})

    return JsonResponse({'status': 'success', 'message': 'El avatar ha sido comprado'})


def equip_a_avatar(request, avatar_id):
    """Controlador que equipa un avatar"""
    user = request.user

    if equip_avatar(user, avatar_id) is None:
        return JsonResponse({'status': 'error', 'message': 'Ha ocurrido un error al equipar el avatar'})

    return JsonResponse({'status': 'success', 'message': 'El avatar ha sido equipado'})
