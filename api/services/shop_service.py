from datetime import datetime

from django.db.models import Count, Q

from api.models import Avatar, UserTransaction, HighlightedList, UserAvatar
from api.services.list_service import get_list


def get_avatar(avatar_id):
    """Obtiene un avatar por su ID"""
    try:
        return Avatar.objects.get(id=avatar_id)
    except Avatar.DoesNotExist:
        return None


def get_all_avatars():
    """Obtiene todos los avatares ordenados por rareza"""
    return Avatar.objects.all().order_by('rarity_id')


def get_avatars_by_popularity():
    """Obtiene los avatares por popularidad"""
    return Avatar.objects.annotate(
            popularity=Count('user__avatar')
        ).order_by('-popularity')


def get_avatars_by_bought(user_id):
    """Obtiene los avatares por compras"""
    return Avatar.objects.annotate(
        user_have_bought=Count('useravatar', filter=Q(useravatar__user_id=user_id) | Q(rarity__id=1))
    ).order_by('-user_have_bought')


def buy_avatar(user, avatar_id):
    """Compra un avatar"""
    avatar = get_avatar(avatar_id)

    # Si el usuario ya tiene el avatar, no se realiza la compra
    if UserAvatar.objects.filter(user=user, avatar=avatar).exists():
        return None

    if avatar is not None and user is not None:
        transaction = UserTransaction.objects.first()  # TODO: Realizar transacción y devolver el objeto

        if transaction is not None:
            UserAvatar.objects.create(user=user, avatar=avatar, transaction=transaction)
            return user.avatar

    return None


def equip_avatar(user, avatar_id):
    """Equipa un avatar"""
    avatar = get_avatar(avatar_id)

    # Si el usuario no tiene el avatar, no se realiza la equipación
    if not UserAvatar.objects.filter(user=user, avatar=avatar).exists():
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


def do_transaction(user, value, date, details):
    """Realiza una transacción"""
    if user is not None:
        transaction = UserTransaction()
        transaction.user = user
        transaction.value = value
        transaction.date = date
        transaction.details = details
        transaction.save()
        return transaction

    return None


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
