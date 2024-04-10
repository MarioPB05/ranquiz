from functools import wraps

from django.http import HttpResponseRedirect


def partial_login_required(function):
    @wraps(function)
    def wrap(request, share_code, *args, **kwargs):
        card = request.GET.get('card', 'resume')

        if (card != 'resume' and share_code != request.user.share_code) or not request.user.is_authenticated:
            return HttpResponseRedirect('/user/' + request.user.share_code + '/?card=' + card)

        return function(request, share_code, *args, **kwargs)

    return wrap
