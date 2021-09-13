from django.http import Http404
from functools import wraps


def is_admin(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name='admins').exists():
            raise Http404()
        return view(request, *args, **kwargs)
    return wrapper

