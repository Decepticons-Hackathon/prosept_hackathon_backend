from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerListTestClass(ApiTestsClass):
    url = '/api/v1/product-to-matched-list/'

    @tag('api', 'product-to-matched-list')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('dealer_products'), list)
        self.assertEqual(data.get('dealer_products_count'), 2)

        products = data.get('dealer_products')
        for product in products:
            self.assertIsInstance(product, dict)
            self.assertIsInstance(product.get('procreator_variants'), list)

        product = products[1].get('dealer_product')

        self.assertEqual(product.get('id'), 5)
        self.assertEqual(product.get('dealer').get('name'), 'Dealer 2')
        self.assertEqual(product.get('product_name'), 'Product 5')
        self.assertEqual(product.get('price'), 205.0)

        self.assertIsInstance(product.get('dealer_product_status'), dict)
        self.assertEqual(product.get('dealer_product_status').get('status'), 'none')

        self.assertIsInstance(product.get('dealer_product_history'), list)
        self.assertEqual(product.get('dealer_product_history')[0].get('status_type'), 'none')

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
