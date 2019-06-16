from django.http import HttpRequest
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseNotFound
from functools import wraps


def allow_method(methods: list):
    def __decorator(func):
        @wraps(func)
        def __wrapper(request: HttpRequest, *args, **kwargs):
            if request.method not in methods:
                return HttpResponseNotAllowed(methods)
            else:
                return func(request, *args, **kwargs)
        return __wrapper
    return __decorator