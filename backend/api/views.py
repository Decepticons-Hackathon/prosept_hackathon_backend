from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.models import (CORRECT_CONDITIONS, Dealer, DealerPrice, DealerProduct,
                        DealerProductStausChange, DealerProductStausHistory,
                        Product)
from api.serializers.response_serializers import (
    DealerDetailResponseSerializer, DealerListResponseSerializer,
    DealerProductListResponseSerializer, DealerProductStatResponseSerializer,
    ProductListResponseSerializer, ProductListToMatchesResponseSerializer)
from api.utils import JsonResponse, force_int

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
        data = {}
        params = request.GET
        query = DealerProductStausChange.objects.filter(
            status=CORRECT_CONDITIONS[2][0]
        )
        data['products_count'] = query.count()
        data['offset'] = force_int(params.get('offset', 0))
        data['limit'] = force_int(params.get('limit', data['products_count']))
        data['data'] = query[data['offset']: data['offset'] + data['limit']]
        serializer = ProductListToMatchesResponseSerializer(data)
        return JsonResponse(serializer.data)


class DealerProductList(APIView):

    @swagger_auto_schema(
        responses={200: ProductListToMatchesResponseSerializer}
    )
    def get(self, request):
        """
        Выводит список товаров диллеров
        """
        data = {}
        params = request.GET
        query = DealerProductStausChange.objects.order_by('id')
        data['products_count'] = query.count()
        data['offset'] = force_int(params.get('offset', 0))
        data['limit'] = force_int(params.get('limit', data['products_count']))
        data['data'] = query[data['offset']: data['offset'] + data['limit']]
        serializer = DealerProductListResponseSerializer(data)
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


class MlForceUpdate(APIView):
    def get(self, request):
        """
        Принудительное обновление рекомендаций
        """
        # TODO: сделать через Celery либо threads
        # MlMatches().get_ml_variants()
        return JsonResponse({}, message='Ok')
