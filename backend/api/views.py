from rest_framework import status
from rest_framework.views import APIView

from api.models import Dealer, Product, DealerPrice, DealerProduct
from api.utils import JsonResponse, Matches
from api.serializers import DealerSerializer, ProductListSerializer


class ProductList(APIView):
    def get(self, request):
        """
        Выводит список неразмеченных товаров
        """
        #TODO: сделать по проекту фронтов
        data = Product.objects.all()
        serializer = ProductListSerializer(data, many=True)
        response = {
            'products': serializer.data,
            'products_count': len(data),
        }
        return JsonResponse(response)


class ProductListMatches(APIView):
    def get(self, request):
        """
        Выводит список размеченных товаров
        """
        return JsonResponse({})


class ProductDetail(APIView):
    def get(self, request, pk):
        """
        Выводит детализацию товара либо совпадение для разметки
        """
        #TODO: добавить обработку смапленных
        try:
            data = Product.objects.get(product_id=pk)
        except Product.DoesNotExist:
            return JsonResponse(
                {},
                code=status.HTTP_404_NOT_FOUND,
                message='Объект не найден'
            )
        serializer = ProductListSerializer(data)
        response = {
            'product_detail': serializer.data
        }
        return JsonResponse(response)

    def post(self, request):
        """
        Метод сопоставления товара образцу (действие разметки)
        """
        return JsonResponse({})


class DealerList(APIView):
    def get(self, request):
        """
        Выводит список диллеров
        """
        data = Dealer.objects.all().order_by('id')
        serializer = DealerSerializer(data, many=True)
        response = {
            'dealers': serializer.data,
            'dealers_count': len(data),
        }
        return JsonResponse(response)


class DealerDetail(APIView):
    def get(self, request, pk):
        """
        Выводит список товаров диллера
        """
        return JsonResponse({})


class ProductsStat(APIView):
    def get(self, request, pk):
        """
        Выводит статистику по размеченным товарам
        """
        return JsonResponse({})


class OperatorStat(APIView):
    def get(self, request, pk):
        """
        Выводит статистику по оператору
        """
        return JsonResponse({})
