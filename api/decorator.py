from django.http import HttpRequest
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from functools import wraps
from .models import *
import json
from json.decoder import JSONDecodeError


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


def get_user(want_user: str):
    def __decorator(func):
        @wraps(func)
        def __wrapper(request:HttpRequest, *args, **kwargs):
            try:
                req = json.loads(request.body.decode())
                user_id = req[want_user]
            except (JSONDecodeError, KeyError, ValueError):
                return HttpResponseBadRequest()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponseNotFound()
            return func(request, user, *args, **kwargs)
        return __wrapper
    return __decorator


def get_post(func):
    @wraps(func)
    def __wrapper(request:HttpRequest, post_id: int, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return HttpResponseNotFound()
        return func(request, post, *args, **kwargs)
    return __wrapper
    

def get_comment(func):
    @wraps(func)
    def __wrapper(request:HttpRequest, comment_id: int, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment)
        except Comment.DoesNotExist:
            return HttpResponseNotFound()
        return func(request, comment, *args, **kwargs)
    return __wrapper


def get_post_user(func):
    @wraps(func)
    def __wrapper(request:HttpRequest, post_id: int, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return HttpResponseNotFound()
        try:
            req = json.loads(request.body.decode())
            user_id = req['user']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponseNotFound()
        return func(Post, User)
    return __wrapper