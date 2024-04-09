from api.models import UserTransaction


def do_transaction(user, value, details):
    """Realiza una transacción de monedas a un usuario"""
    transaction = UserTransaction(user=user, value=value, details=details)
    transaction.save()
    return id(transaction)
