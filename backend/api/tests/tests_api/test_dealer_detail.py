from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerDetailTestClass(ApiTestsClass):
    url = '/api/v1/dealer-detail/2/'

    @tag('api', 'dealer-detail')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('dealer'), dict)
        self.assertIsInstance(data.get('dealer_products'), list)
        self.assertEqual(data.get('dealer_products_count'), 1)
        self.assertEqual(data.get('dealer').get('id'), 2)
        self.assertEqual(data.get('dealer').get('name'), 'Dealer 2')

        dealer_product = data.get('dealer_products')[0].get('product')

        self.assertEqual(dealer_product.get('id'), 2)
        self.assertEqual(dealer_product.get('article'), '242-12')
        self.assertEqual(dealer_product.get('name_1c'), 'Product 2')

        dealer_product_info = data.get('dealer_products')[0].get('dealer_product_info')

        self.assertIsInstance(dealer_product_info, list)
        self.assertIsInstance(dealer_product_info[0].get('dealer_product_history'), list)
        self.assertIsInstance(dealer_product_info[0].get('dealer_product_status'), dict)
        self.assertEqual(dealer_product_info[0].get('price'), 175.0)
        self.assertEqual(dealer_product_info[0].get('date'), '2023-07-11')

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
