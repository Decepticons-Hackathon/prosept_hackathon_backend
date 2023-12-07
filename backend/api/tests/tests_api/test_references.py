from django.test import tag
from rest_framework import status

from api.tests.utils import ApiTestsClass


class DealerDetailTestClass(ApiTestsClass):
    url = '/api/v1/references/'

    @tag('api', 'references')
    def test_dealer_list(self):

        data = self.get_api()

        self.assertIsInstance(data, dict)
        self.assertIsInstance(data.get('conditions'), list)
        self.assertIsInstance(data.get('status_types'), list)

        self.assertEqual(data.get('conditions')[0], {'approve': 'Подтвердить'})
        self.assertEqual(data.get('status_types')[1], {'manual': 'Поиск в ручную'})

    def get_api(self):

        response = self.call_api('get', self.url)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('code'), status.HTTP_200_OK)
        self.assertIsInstance(response.get('data'), dict)

        data = response.get('data')
        return data
