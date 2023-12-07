from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerDetailTestClass(ApiTestsClass):
    url = '/api/v1/dealers-stat/'

    @tag('api', 'dealers-stat')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('dealers'), list)

        dealer = data.get('dealers')[1]

        self.assertIsInstance(dealer.get('dealer'), list)
        self.assertEqual(dealer.get('dealer')[0].get('name'), 'Dealer 2')
        self.assertEqual(dealer.get('stat_all').get('approve'), 2)
        self.assertEqual(dealer.get('stat_all').get('aside'), 0)
        self.assertEqual(dealer.get('stat_all').get('none'), 2)

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
