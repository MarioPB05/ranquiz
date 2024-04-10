from functools import wraps

from django.http import HttpResponseRedirect


def partial_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        card = request.GET.get('card', 'resume')

        if card != 'resume' and not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')

        return function(request, *args, **kwargs)

    return wrap
