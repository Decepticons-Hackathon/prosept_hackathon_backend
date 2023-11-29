from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerDetailTestClass(ApiTestsClass):
    url = '/api/v1/dealer-detail/2/'

    @tag('api')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data.get('dealer'), dict)
        self.assertIsInstance(data.get('dealer_products'), list)
        self.assertEqual(data.get('dealer_products_count'), 67)
        self.assertEqual(data.get('dealer').get('id'), 2)
        self.assertEqual(data.get('dealer').get('name'), 'Akson')

        dealer_product = data.get('dealer_products')[0].get('product')

        self.assertEqual(dealer_product.get('product_id'), 339)
        self.assertEqual(dealer_product.get('article'), '040-9')
        self.assertEqual(dealer_product.get('ean_13'), '4680008145987.0')
        self.assertEqual(
            dealer_product.get('name'),
            'Антисептик лессирующий BiO LASUR / тик / 9 л'
        )
        self.assertIsInstance(dealer_product.get('dealer_prices'), list)
        self.assertIsInstance(dealer_product.get('dealer_prices')[0], dict)
        self.assertEqual(
            dealer_product.get('dealer_prices')[0].get('price'),
            233.0
        )
        self.assertEqual(
            dealer_product.get('dealer_prices')[0].get('date'),
            '2023-07-11'
        )

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
