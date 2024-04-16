from datetime import datetime

from django.db.models import Count, Q, Case, When, Exists, OuterRef

from api.models import Avatar, UserTransaction, HighlightedList, UserAvatar
from api.services.list_service import get_list
from api.services.transaction_service import do_transaction


def get_avatar(avatar_id):
    """Obtiene un avatar por su ID"""
    try:
        return Avatar.objects.get(id=avatar_id)
    except Avatar.DoesNotExist:
        return None


def get_all_avatars(user):
    """Obtiene todos los avatares ordenados por rareza"""

    if user is None:
        return None

    return Avatar.objects.annotate(
        is_user_avatar=Exists(
            UserAvatar.objects.all().filter(avatar=OuterRef('pk'), user=user)
        )
    ).order_by('rarity_id')

def get_avatars_by_popularity():
    """Obtiene los avatares por popularidad"""
    return Avatar.objects.annotate(
            popularity=Count('user__avatar')
        ).order_by('-popularity')


def get_avatars_by_purchased(user_id):
    """Obtiene los avatares por compras"""
    return Avatar.objects.annotate(
        user_have_bought=Count('useravatar', filter=Q(useravatar__user_id=user_id) | Q(rarity__id=1))
    ).order_by('-user_have_bought')
    ).annotate(
        user_have_bought=Count('useravatar', filter=Q(useravatar__user_id=user.id))
    ).order_by(
        Case(
            When(Q(rarity__id=1) | Q(user_have_bought__gt=0), then=0),  # Avatares con rareza 1 o comprados por el usuario primero
            default=1  # Todos los demás después
        ),
        '-user_have_bought'  # Luego, ordenar por la cantidad de compras asociadas al usuario (en orden descendente)
    )


def buy_avatar(user, avatar_id):
    """Compra un avatar"""
    avatar = get_avatar(avatar_id)

    # Si el usuario ya tiene el avatar, no se realiza la compra
    if avatar.rarity.id == 1 or UserAvatar.objects.filter(user=user, avatar=avatar).exists():
        return None

    if avatar is not None and user is not None:
        transaction = do_transaction(user, -avatar.rarity.price, "Avatar comprado")

        if transaction is not None:
            UserAvatar.objects.create(user=user, avatar=avatar, transaction=transaction)
            return user.avatar

    return None


def equip_avatar(user, avatar_id):
    """Equipa un avatar"""
    avatar = get_avatar(avatar_id)

    # Si el usuario no tiene el avatar, no se realiza la equipación
    if avatar.rarity.id != 1 and not UserAvatar.objects.filter(user=user, avatar=avatar).exists():
        return None

    if avatar is not None and user is not None:
        user.avatar = avatar
        user.save()
        return user.avatar

    return None


def calculate_highlight_price(start_date, end_date):
    """Calcula el precio de destacar una lista"""
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    total_price = 0
    days = (end_date - start_date).days

    if days >= 1:
        total_price = 15
        days -= 1

    while days > 0:
        total_price += 10
        days -= 1

    return total_price


def highlight_list(share_code, start_date, end_date):
    """Destaca una lista"""
    # Obtenemos la lista
    required_list = get_list(share_code)

    if required_list is not None:
        transaction = do_transaction(
            required_list.user,
            -(calculate_highlight_price(start_date, end_date)),
            datetime.now(),
            'Destacar lista')

        if transaction is not None:
            highlighted_list = HighlightedList()
            highlighted_list.list = required_list
            highlighted_list.start_date = start_date
            highlighted_list.end_date = end_date
            highlighted_list.save()
            return highlighted_list

        # TODO: Administrar errores
        return None

    return None
