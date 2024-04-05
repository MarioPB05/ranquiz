from api.models import Avatar


def get_avatar(avatar_id):
    """Obtiene un avatar por su ID"""
    try:
        return Avatar.objects.get(id=avatar_id)
    except Avatar.DoesNotExist:
        return None
