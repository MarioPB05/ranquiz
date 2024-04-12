from api.models import UserTransaction, User


def do_transaction(user, value, details):
    """Realiza una transacción de monedas a un usuario"""
    if not validate_transaction(user, value):
        return None

    transaction = UserTransaction(user=user, value=value, details=details)
    transaction.save()

    user.money += value
    return id(transaction)


def validate_transaction(user, value):
    """Valida una transacción"""
    if value >= 0:
        return True

    if user is not None and value is not None:
        return User.money >= (-value)

    return False
