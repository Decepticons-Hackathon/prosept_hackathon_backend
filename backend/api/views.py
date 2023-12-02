from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.models import (CORRECT_CONDITIONS, Dealer, DealerPrice, DealerProduct,
                        DealerProductStausChange, DealerProductStausHistory,
                        Product)
from api.serializers.response_serializers import (
    DealerDetailResponseSerializer, DealerListResponseSerializer,
    DealerProductStatResponseSerializer, ProductListResponseSerializer,
    ProductListToMatchesResponseSerializer)
from api.utils import JsonResponse

# TODO: Разобраться почему @swagger_auto_schema не работает

class ProductList(APIView):

    @swagger_auto_schema(responses={200: ProductListResponseSerializer})
    def get(self, request):
        """
        Выводит список товаров
        """
        data = Product.objects.all()
        serializer = ProductListResponseSerializer(data)
        return JsonResponse(serializer.data)


class ProductListToMatches(APIView):

    @swagger_auto_schema(
        responses={200: ProductListToMatchesResponseSerializer}
    )
    def get(self, request):
        """
        Выводит список не размеченных товаров
        """
        data = DealerProductStausChange.objects.filter(
            status=CORRECT_CONDITIONS[2][0]
        )
        serializer = ProductListToMatchesResponseSerializer(data)
        return JsonResponse(serializer.data)


class ProductDetail(APIView):

    # @swagger_auto_schema(responses={200: ProductSerializer})
    def post(self, request):
        """
        Метод сопоставления товара образцу (действие разметки)
        """
        return JsonResponse({})


class DealerList(APIView):

    @swagger_auto_schema(responses={200: DealerListResponseSerializer})
    def get(self, request):
        """
        Выводит список диллеров
        """
        data = Dealer.objects.all()
        serializer = DealerListResponseSerializer(data)
        return JsonResponse(serializer.data)


class DealerDetail(APIView):

    # добавить в сваггер 404
    @swagger_auto_schema(responses={200: DealerDetailResponseSerializer})
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
        serializers = DealerDetailResponseSerializer(dealer_products)
        return JsonResponse(serializers.data)


class ProductsStat(APIView):

    # добавить в сваггер 404
    @swagger_auto_schema(responses={200: DealerProductStatResponseSerializer})
    def get(self, request, pk):
        """
        Выводит статистику по размеченным товарам
        """
        try:
            dealer_product = DealerPrice.objects.get(id=pk)
        except DealerPrice.DoesNotExist:
            return JsonResponse(code=404, message='Объект не найден')
        try:
            data = DealerProductStausHistory.objects.filter(
                dealer_product_id=dealer_product
            )
        except DealerProductStausHistory.DoesNotExist:
            return JsonResponse(code=404, message='Объект не найден')
        serializer = DealerProductStatResponseSerializer(data)
        return JsonResponse(serializer.data)
