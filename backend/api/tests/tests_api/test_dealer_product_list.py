from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerListTestClass(ApiTestsClass):
    url = '/api/v1/dealer-product-list/'

    @tag('api', 'dealer-product-list')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('product_list'), list)
        self.assertEqual(data.get('products_count'), 5)
        self.assertEqual(data.get('offset'), 0)
        self.assertEqual(data.get('limit'), 5)

        products = data.get('product_list')
        for product in products:
            self.assertIsInstance(product, dict)
            self.assertIsInstance(product.get('procreator_variants'), list)

        product = products[1].get('dealer_product')

        self.assertIsInstance(product.get('procreator_product'), dict)
        self.assertEqual(product.get('procreator_product').get('id'), 2)
        self.assertEqual(product.get('procreator_product').get('name_1c'), 'Product 2')

        self.assertIsInstance(product.get('dealer_product_info'), dict)
        self.assertEqual(product.get('dealer_product_info').get('price'), 175.0)
        self.assertEqual(product.get('dealer_product_info').get('product_name'), 'Product 2')
        
        self.assertIsInstance(product.get('dealer_product_info').get('dealer_product_history'), list)
        self.assertIsInstance(product.get('dealer_product_info').get('dealer_product_status'), dict)
        self.assertEqual(product.get('dealer_product_info').get('dealer_product_status').get('status'), 'approve')

        history = product.get('dealer_product_info').get('dealer_product_history')[0]
        self.assertEqual(history.get('status_type'), 'none')

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
