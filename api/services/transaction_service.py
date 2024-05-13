from api.models import UserTransaction


def do_transaction(user, value, details):
    """Realiza una transacción de monedas a un usuario"""
    if not validate_transaction(user, value):
        return None

    transaction = UserTransaction(user=user, value=value, details=details)
    transaction.save()

    user.money += value
    user.save()
    return transaction


def validate_transaction(user, value):
    """Valida una transacción"""
    if value >= 0:
        return True

    if user is not None and value is not None:
        user_money = user.money
        return user_money >= (-value)

    return False


def refund_transaction(transaction):
    """Reembolsa una transacción"""
    user = transaction.user
    return do_transaction(user, -transaction.value, "Reembolso de transacción") is not None
