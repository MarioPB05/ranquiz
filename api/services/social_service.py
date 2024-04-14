from api.models import UserFollow


def get_followers(user):
    """Obtiene los seguidores de un usuario"""
    return UserFollow.objects.filter(follower=user)


def get_following(user):
    """Obtiene los usuarios que sigue un usuario"""
    return UserFollow.objects.filter(user_followed=user)
