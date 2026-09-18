from functools import wraps

from django.http import Http404

from .models import SiteSettings


def require_section(flag):
    """Return a decorator that 404s a view when the matching section is disabled.

    ``flag`` is the SiteSettings boolean name, e.g. ``show_blog``.
    """

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not getattr(SiteSettings.load(), flag, True):
                raise Http404("This section is disabled.")
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
