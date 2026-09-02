from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """
    Backend-level protection for Admin-only pages (like Profit).
    Even if a Staff user manually types the Profit URL directly
    into the browser, this decorator blocks access with a 403
    Forbidden error — hiding the sidebar link alone is NOT enough.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_role():
            raise PermissionDenied("Only Admin can access the Profit page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view