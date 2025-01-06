from django.http import HttpResponseForbidden
from functools import wraps

def teacher_or_admin_required(view_func):
    """
    Custom decorator to allow access only to teachers or admins.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or hasattr(request.user, 'teacher')):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapper
