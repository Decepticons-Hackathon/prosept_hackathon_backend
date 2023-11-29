from rest_framework.test import APITestCase as TestCase


class ApiTestsClass(TestCase):
    fixtures = ['test_data.json']

    def call_api(
            self, method, url, user={}, *args, **kwargs):
        request_method = getattr(self.client, method)
        response = request_method(url, *args, **kwargs)
        return response.json()
