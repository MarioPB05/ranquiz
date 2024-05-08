from api.models import User


def get_user(user_id=None, share_code=None):
    """Función que obtiene un usuario por su id o su share_code"""
    try:
        if user_id is not None:
            return User.objects.get(id=user_id)

        if share_code is not None:
            return User.objects.get(share_code=share_code)

        return None
    except User.DoesNotExist:
        return None
