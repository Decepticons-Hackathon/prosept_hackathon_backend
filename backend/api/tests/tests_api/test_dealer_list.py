from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerListTestClass(ApiTestsClass):
    url = '/api/v1/dealer-list/'

    @tag('api', 'dealer-list')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('dealers'), list)
        self.assertEqual(data.get('dealers_count'), 3)

        dealers = data.get('dealers')
        for dealer in dealers:
            self.assertIsInstance(dealer, dict)

        self.assertEqual(dealers[2].get('id'), 3)
        self.assertEqual(dealers[2].get('name'), 'Dealer 3')

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
