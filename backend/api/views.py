from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.models import Dealer, DealerProduct, Product
from api.serializers import (DealerProductSerializer, DealerSerializer,
                             ProductSerializer)
from api.utils import JsonResponse


class ProductList(APIView):

    @swagger_auto_schema(responses={200: ProductSerializer})
    def get(self, request):
        """
        Выводит список неразмеченных товаров
        """

        data = Product.objects.all()
        serializer = ProductSerializer(data, many=True)
        response = {
            'products': serializer.data,
            'products_count': len(data),
        }

        return JsonResponse(response)


class ProductListMatches(APIView):

    @swagger_auto_schema(responses={200: ProductSerializer})
    def get(self, request):
        """
        Выводит список размеченных товаров
        """
        return JsonResponse({})


class ProductDetail(APIView):

    @swagger_auto_schema(responses={200: ProductSerializer})
    def get(self, request, pk):
        """
        Выводит детализацию товара либо совпадение для разметки
        """

        # TODO: добавить обработку смапленных
        try:
            data = Product.objects.get(product_id=pk)

        except Product.DoesNotExist:
            return JsonResponse(
                {},
                code=status.HTTP_404_NOT_FOUND,
                message='Объект не найден'
            )

        serializer = ProductSerializer(data)
        response = {
            'product_detail': serializer.data
        }

        return JsonResponse(response)

    @swagger_auto_schema(responses={200: ProductSerializer})
    def post(self, request):
        """
        Метод сопоставления товара образцу (действие разметки)
        """
        return JsonResponse({})


class DealerList(APIView):

    @swagger_auto_schema(responses={200: DealerSerializer})
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

        try:
            dealer = Dealer.objects.get(id=pk)

        except Dealer.DoesNotExist:
            return JsonResponse(
                {},
                code=status.HTTP_404_NOT_FOUND,
                message='Объект не найден'
            )

        dealer_products = DealerProduct.objects.filter(dealer_id=dealer)
        count = len(dealer_products)
        dealer_products_list = []

        for obj in dealer_products:
            dealer_products_list.append(DealerProductSerializer(obj).data)
        response = {
            'dealer': DealerSerializer(dealer).data,
            'dealer_products': dealer_products_list,
            'dealer_products_count': count,
        }

        return JsonResponse(response)


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
