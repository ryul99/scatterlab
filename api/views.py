from .models import *
from .decorator import *
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from json.decoder import JSONDecodeError


@allow_method(['GET', 'POST'])
def article(request: HttpRequest):
    if request.method == 'GET':
        post_list = [post.to_dict() for post in Post.objects.all()]
        return JsonResponse(post_list, safe=False)
    else:
        try:
            req = json.loads(request.body.decode())
            title = req['title']
            post_body = req['post_body']
            writer_id = req['writer']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        try:
            writer = User.objects.get(id=writer_id)
        except User.DoesNotExist:
            return HttpResponseNotFound()
        post = Post(title=title, post_body=post_body, writer=writer)
        post.save()
        return JsonResponse(post.to_dict(), safe=False)


@allow_method(['PUT', 'GET', 'DELETE'])
def specific_article(request: HttpRequest, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    if request.method == 'PUT':
        try:
            req = json.loads(request.body.decode())
            title = req['title']
            post_body = req['post_body']
            user_id = req['user']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponseNotFound()
        if user != post.writer:
            return HttpResponseBadRequest()
        post.title = title
        post.post_body = post_body
        post.save()
        return JsonResponse(post.to_dict(), safe=False)

    if request.method == 'GET':
        return JsonResponse(post.to_dict(), safe=False)

    else:
        try:
            req = json.loads(request.body.decode())
            user_id = req['user']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponseNotFound()
        if user != post.writer:
            return HttpResponseBadRequest()
        post.delete()
        return HttpResponse()


@allow_method(['POST'])
def comment(request: HttpRequest, post_id):
    try:
        post = post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    try:
        req = json.loads(request.body.decode())
        writer_id = req['writer']
        text = req['text']
    except (JSONDecodeError, KeyError, ValueError):
        return HttpResponseBadRequest()
    try:
        writer = User.objects.get(id=writer_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()
    comment = Comment(post = post, writer = writer, text = text)
    comment.save()
    return JsonResponse(comment.to_dict(), safe=False)


@allow_method(['POST'])
@get_post
@get_user
def like_post(user, post):
    post.like_user.add(user)
    return HttpResponse()


@allow_method(['POST'])
@get_post
@get_user
def hate_post(user, post):
    post.hate_user.add(user)
    return HttpResponse()


@allow_method(['POST'])
@get_comment
@get_user
def like_comment(user, comment):
    comment.like_user.add(user)
    return HttpResponse()


@allow_method(['POST'])
@get_comment
@get_user
def hate_comment(user, comment):
    comment.like_user.add(user)
    return HttpResponse()