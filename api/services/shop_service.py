from datetime import datetime

from api.models import Avatar, UserTransaction, HighlightedList
from api.services.list_service import get_list


def get_avatar(avatar_id):
    """Obtiene un avatar por su ID"""
    try:
        return Avatar.objects.get(id=avatar_id)
    except Avatar.DoesNotExist:
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
