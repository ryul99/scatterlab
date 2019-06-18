from django.test import TestCase, Client
from django.db import transaction
import json
from api.models import *
from . import TestCaseWithHttp
from datetime import date


class PostTestCase(TestCaseWithHttp):
    def setUp(self):
        self.user = User(
            sex = 'female',
            nickname = 'ironman',
            profile_photo = 'https://www.google.com',
            birthday = date(2000,2,2),
        )
        self.user.save()

        self.article = Post(
            writer = self.user,
            title = 'title',
            post_body = 'post_body',
        )
        self.article.save()

        self.comment = Comment(
            post = self.article,
            writer = self.user,
            text = "wow",
        )

    def test_not_allowed(self):
        self.assertEqual(self.put('/api/posts/', {}).status_code, 405)
        self.assertEqual(self.delete('/api/posts/', {}).status_code, 405)

        self.assertEqual(self.post('/api/posts/1/', {}).status_code, 405)

        self.assertEqual(self.put('/api/posts/1/like/', {}).status_code, 405)
        self.assertEqual(self.get('/api/posts/1/like/').status_code, 405)
        self.assertEqual(self.delete('/api/posts/1/like/', {}).status_code, 405)
        self.assertEqual(self.put('/api/posts/1/hate/', {}).status_code, 405)
        self.assertEqual(self.get('/api/posts/1/hate/').status_code, 405)
        self.assertEqual(self.delete('/api/posts/1/hate/', {}).status_code, 405)
        
        self.assertEqual(self.put('/api/comments/1/like/', {}).status_code, 405)
        self.assertEqual(self.get('/api/comments/1/like/').status_code, 405)
        self.assertEqual(self.delete('/api/comments/1/like/', {}).status_code, 405)        
        self.assertEqual(self.put('/api/comments/1/hate/', {}).status_code, 405)
        self.assertEqual(self.get('/api/comments/1/hate/').status_code, 405)
        self.assertEqual(self.delete('/api/comments/1/hate/', {}).status_code, 405)


    def test_get_articles(self):
        resp = self.get('/api/posts/')
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEqual(resp_json, [self.article.to_dict()])

    def test_post_article(self):
        self.assertEqual(self.post('/api/posts/', {}).status_code, 400)
        self.assertEqual(self.post('/api/posts/', {'writer': 44, 'title': "h", 'post_body': "h"}).status_code, 404)

        new_post = {
            'writer': self.user.id,
            'title': 'hi',
            'post_body': 'hell',
        }
        resp = self.post('/api/posts/', new_post)
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEqual(resp_json['writer'], new_post['writer'])
        self.assertEqual(resp_json['title'], new_post['title'])
        self.assertEqual(resp_json['post_body'], new_post['post_body'])

    def test_put_article(self):
        self.assertEqual(self.put('/api/posts/44/', {}).status_code, 404)
        self.assertEqual(self.put('/api/posts/1/', {}).status_code, 400)
        self.assertEqual(self.put('/api/posts/1/', {'user': 44, 'title': "h", 'post_body': "h"}).status_code, 404)

        User(
            sex = 'male',
            nickname = 'milk',
            profile_photo = 'https://www.google.com',
            birthday = date(2000,2,2),
        ).save()
        self.assertEqual(self.put('/api/posts/1/', {'user': 2, 'title': "h", 'post_body': "h"}).status_code, 400)

        new_post = {
            'user': self.user.id,
            'title': 'hi',
            'post_body': 'hell',
        }

        resp = self.put('/api/posts/1/', new_post)
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEqual(resp_json['writer'], new_post['user'])
        self.assertEqual(resp_json['title'], new_post['title'])
        self.assertEqual(resp_json['post_body'], new_post['post_body'])

    def test_get_article(self):
        self.assertEqual(self.get('/api/posts/44/').status_code, 404)
        resp = self.get('/api/posts/1/')
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEqual(resp_json['writer'], self.article.to_dict()['writer'])
        self.assertEqual(resp_json['title'], self.article.to_dict()['title'])
        self.assertEqual(resp_json['post_body'], self.article.to_dict()['post_body'])

    def test_delete_article(self):
        self.assertEqual(self.delete('/api/posts/44/', {}).status_code, 404)
        self.assertEqual(self.delete('/api/posts/1/', {}).status_code, 400)
        self.assertEqual(self.delete('/api/posts/1/', {'user': 44}).status_code, 404)
        
        User(
            sex = 'male',
            nickname = 'uyu',
            profile_photo = 'https://www.google.com',
            birthday = date(2000,2,2),
        )
        self.assertEqual(self.delete('/api/posts/1/', {'user': 2}).status_code, 404)

        self.assertEqual(self.delete('/api/posts/1/', {'user': 1}).status_code, 200)

    def test_comment(self):
        self.assertEqual(self.post('/api/posts/44/comment/', {}).status_code, 404)
        self.assertEqual(self.post('/api/posts/1/comment/', {}).status_code, 400)
        self.assertEqual(self.post('/api/posts/1/comment/', {'writer': 11, 'text': 'uyu joa'}).status_code, 404)
        
        new_comment = {'writer': 1, 'text': 'uyu joa'}
        resp = self.post('/api/posts/1/comment/', new_comment)
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEqual(resp_json['writer'], new_comment['writer'])
        self.assertEqual(resp_json['text'], new_comment['text'])

    def like_post(self):
        self.like_hate_test('posts', 'like', 'like_user')

    def hate_post(self):
        self.like_hate_test('posts', 'hate', 'hate_user')

    def like_comment(self):
        self.like_hate_test('comments', 'like', 'like_user')

    def hate_comment(self):
        self.like_hate_test('comments', 'hate', 'like_user')