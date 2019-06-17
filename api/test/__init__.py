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