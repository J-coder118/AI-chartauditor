from django.shortcuts import redirect
from functools import wraps


def profile_completion_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_profile:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('custom_login')

    return wrapper
