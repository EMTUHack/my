from functools import wraps
from django.http import HttpResponseForbidden


def require_condition(condition=True):
    def decorator(function):
        @wraps(function)
        def check_value(self, *args, **kwargs):
            if condition:
                return function(self, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        return check_value
    return decorator
