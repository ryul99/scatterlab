from django.test import TestCase, Client
from django.db import transaction
import json


class TestCaseWithHttp(TestCase):
    def setUp(self):
        super().setUp()

    def get(self, url):
        return self.client.get(url)

    def post(self, url, obj):
        return self.client.post(url, json.dumps(obj), content_type='application/json')

    def put(self, url, obj):
        return self.client.put(url, json.dumps(obj), content_type='application/json')

    def delete(self, url, obj):
        return self.client.delete(url, json.dumps(obj), content_type='application/json')

    def like_hate_test(self, obj, emo, emo_list):
        self.assertEqual(self.post('/api/{0}/44/{1}/'.format(obj, emo), {}).status_code, 404)
        self.assertEqual(self.post('/api/{0}/1/{1}/'.format(obj, emo), {}).status_code, 400)
        self.assertEqual(self.post('/api/{0}/1/{1}/'.format(obj, emo), {'user': 2}).status_code, 404)
        self.assertEqual(self.post('/api/{0}/1/{1}/'.format(obj, emo), {'user': 1}).status_code, 200)
        self.assertEqual(len(getattr(self.post1, emo_list).filter(id = 1)), 1)