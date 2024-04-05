from datetime import datetime

from api.models import Avatar


def get_avatar(avatar_id):
    """Obtiene un avatar por su ID"""
    try:
        return Avatar.objects.get(id=avatar_id)
    except Avatar.DoesNotExist:
        return None


def calculate_highlight_price(start_date, end_date):
    """Calcula el precio de destacar una lista"""
    start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
    end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

    total_price = 0
    days = (end_date - start_date).days

    if days >= 1:
        total_price = 15
        days -= 1

    while days > 0:
        total_price += 10
        days -= 1

    return total_price
