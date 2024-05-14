from functools import wraps

from django.http import HttpResponseRedirect
from django.urls import reverse


def partial_login_required(function):
    """Decorador para la página de perfil de usuario"""
    @wraps(function)
    def wrap(request, *args, share_code=None, **kwargs):
        card = request.GET.get('card', 'resume')
        user_share_code = request.user.share_code if request.user.is_authenticated else None

        if not request.user.is_authenticated and share_code is None:
            return HttpResponseRedirect(reverse('homepage'))

        if card != 'resume' and share_code != user_share_code:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('user', kwargs={'share_code': share_code}))

            return HttpResponseRedirect('/user/' + user_share_code + '/?card=' + card)

        return function(request, share_code, *args, **kwargs)

    return wrap
