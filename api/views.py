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
            writer = req['writer']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        post = Post(title=title, post_body=post_body, writer=writer)
        post.save()
        return JsonResponse(post.to_dict(), safe=False)


@allow_method(['PUT', 'GET', 'DELETE'])
def specific_article(request: HttpRequest, post_id):
    try:
        post = post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    if request.method == 'PUT':
        try:
            req = json.loads(request.body.decode())
            title = req['title']
            post_body = req['post_body']
            writer = req['writer']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        if writer != post.writer:
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
            writer = req['writer']
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()
        if writer != post.writer:
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
        writer = req['writer']
        text = req['text']
    except (JSONDecodeError, KeyError, ValueError):
        return HttpResponseBadRequest()
    comment = Comment(post = post, writer = writer, text = text)


@allow_method(['POST'])
def like_post(request: HttpRequest, post_id):
    try:
        post = post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    try:
        req = json.loads(request.body.decode())
        user = req['user']
    except (JSONDecodeError, KeyError, ValueError):
        return HttpResponseBadRequest()
    post.like_user.add