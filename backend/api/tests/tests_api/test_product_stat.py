from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerDetailTestClass(ApiTestsClass):
    url = '/api/v1/product-stat/3/'

    @tag('api', 'product_stat')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data, dict)
        self.assertIsInstance(data.get('dealer_product'), dict)

        product = data.get('dealer_product')
        self.assertEqual(product.get('id'), 3)
        self.assertEqual(product.get('dealer'), {'id': 3, 'name': 'Dealer 3'})
        self.assertEqual(product.get('product_name'), 'Product 3')
        self.assertEqual(product.get('dealer_product_status').get('status'), 'approve')
        self.assertIsInstance(product.get('dealer_product_history'), list)
        self.assertEqual(product.get('dealer_product_history')[0].get('status_type'), 'none')

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
