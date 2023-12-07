from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerDetailTestClass(ApiTestsClass):
    url = '/api/v1/match-stat/'

    @tag('api', 'match-stat')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data, dict)

        self.assertEqual(data.get('ds'), 1)
        self.assertEqual(data.get('manual'), 2)
        self.assertEqual(data.get('cancel'), 0)
        self.assertEqual(data.get('var_1'), 1)

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
