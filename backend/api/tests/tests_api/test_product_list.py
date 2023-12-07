from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerListTestClass(ApiTestsClass):
    url = '/api/v1/product-list/'

    @tag('api', 'product-list')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('products'), list)
        self.assertEqual(data.get('products_count'), 5)

        products = data.get('products')
        for product in products:
            self.assertIsInstance(product, dict)

        self.assertEqual(products[2].get('id'), 3)
        self.assertEqual(products[2].get('name'), 'Product 3')
        self.assertEqual(products[2].get('cost'), 307.0)
        self.assertEqual(products[2].get('ean_13'), '4680008145208.0')
        self.assertEqual(products[2].get('ym_article'), '0024-06-с')

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
