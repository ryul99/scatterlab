from .models import *
from .decorator import *
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from json.decoder import JSONDecodeError


@allow_method(['GET', 'POST'])
def post(request: HttpRequest):
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
@get_post
def specific_post(request: HttpRequest, post: Post):
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
        if user.id != post.writer.id:
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
        if user.id != post.writer.id:
            return HttpResponseBadRequest()
        post.delete()
        return HttpResponse()


@allow_method(['POST'])
@get_post
@get_user('writer')
def comment(request: HttpRequest, writer: User, post: Post):
    try:
        req = json.loads(request.body.decode())
        text = req['text']
    except (JSONDecodeError, KeyError, ValueError):
        return HttpResponseBadRequest()
    comment = Comment(post = post, writer = writer, text = text)
    comment.save()
    return JsonResponse(comment.to_dict(), safe=False)


@allow_method(['POST'])
@get_post
@get_user('user')
def like_post(request, user, post):
    post.like_user.add(user)
    return HttpResponse()


@allow_method(['POST'])
@get_post
@get_user('user')
def hate_post(request, user, post):
    post.hate_user.add(user)
    return HttpResponse()


@allow_method(['POST'])
@get_comment
@get_user('user')
def like_comment(request, user, comment):
    comment.like_user.add(user)
    return HttpResponse()


@allow_method(['POST'])
@get_comment
@get_user('user')
def hate_comment(request, user, comment):
    comment.like_user.add(user)
    return HttpResponse()