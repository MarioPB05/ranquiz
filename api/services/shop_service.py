from datetime import datetime

from django.db.models import Count, Q, Case, When, Exists, OuterRef

from api.models import Avatar, HighlightedList, UserAvatar, List
from api.services.transaction_service import do_transaction, refund_transaction


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


def get_avatars_by_popularity(user):
    """Obtiene los avatares por popularidad"""
    if user is None:
        return None

    return Avatar.objects.annotate(
        is_user_avatar=Exists(
            UserAvatar.objects.all().filter(avatar=OuterRef('pk'), user=user)
        )
    ).annotate(
            popularity=Count('user__avatar')
        ).order_by('-popularity')


def get_avatars_by_purchased(user):
    """Obtiene los avatares por compras"""
    if user is None:
        return None

    return Avatar.objects.annotate(
        is_user_avatar=Exists(
            UserAvatar.objects.all().filter(avatar=OuterRef('pk'), user=user)
        )
    ).annotate(
        user_have_bought=Count('useravatar', filter=Q(useravatar__user_id=user.id))
    ).order_by(
        Case(
            # Avatares con rareza 1 o comprados por el usuario primero
            When(Q(rarity__id=1) | Q(user_have_bought__gt=0), then=0),
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


def list_is_highlighted(share_code):
    """Servicio que comprueba si una lista está destacada"""
    start_date = datetime.now()
    end_date = datetime.now()
    lit_obj = List.get(share_code)

    if lit_obj is None:
        return None

    return HighlightedList.objects.filter(list=lit_obj,
                                          start_date__lte=start_date,
                                          end_date__gte=end_date).exists()


def highlight_list(user, share_code, start_date, end_date):
    """Servicio que destaca una lista"""
    list_obj = List.get(share_code)

    if list_obj is None or start_date is None or end_date is None or\
            start_date > end_date or not list_obj.public:
        return False

    value = calculate_highlight_price(start_date, end_date)

    if value <= 0:
        return False

    transaction = do_transaction(user, -value, "Destacar lista")

    if transaction is None:
        return False

    # Para que la fecha de fin a las 23:59:59
    end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    highlighted_list = HighlightedList(list=list_obj, start_date=start_date, end_date=end_date, transaction=transaction)
    highlighted_list.save()

    if highlighted_list is None:
        refund_transaction(transaction)
        return False

    return True
