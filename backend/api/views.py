import logging

from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.models import (
    CORRECT_CONDITIONS,
    STATUS_TYPE,
    Dealer,
    DealerPrice,
    DealerProduct,
    DealerProductStausChange,
    DealerProductStausHistory,
    DealerProductVariants,
    Product
)
from api.serializers.response_serializers import (
    DealerDetailResponseSerializer, DealerListResponseSerializer,
    DealerProductListResponseSerializer, DealerProductStatResponseSerializer,
    ProductListResponseSerializer, ProductListToMatchesResponseSerializer)
from api.utils import JsonResponse, force_int


logger = logging.getLogger(__name__)

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
            status=CORRECT_CONDITIONS[3][0]
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


class ProductMatching(APIView):
    @transaction.atomic
    def _set_approve(self, params, dealer_product, is_manual):
        product_id = force_int(params.get('product_id', 0))
        product = Product.objects.get(id=product_id)
        dealer = Dealer.objects.get(id=dealer_product.dealer_id)
        product_match, _ = DealerProduct.objects.get_or_create(
            product_id=product,
            dealer_id=dealer,
        )
        product_match.key.add(dealer_product)
        product_match.save()
        if is_manual == 'False':
            obj_variant = DealerProductVariants.objects.get(
                dealer_product_id=dealer_product,
                product_id=product
            )
            DealerProductStausHistory.objects.create(
                dealer_product_id=dealer_product,
                status_type=STATUS_TYPE[0][0],
                product_variant=obj_variant
            )
        else:
            DealerProductStausHistory.objects.create(
                dealer_product_id=dealer_product,
                status_type=STATUS_TYPE[1][0]
            )
        obj = DealerProductStausChange.objects.get(dealer_product_id=dealer_product)
        obj.product_id = product
        obj.status = CORRECT_CONDITIONS[0][0]
        obj.status_datetime = timezone.now()
        obj.save()
        return

    @transaction.atomic
    def _set_not_approve(self, button, dealer_product):
        def _set_status_and_history(product_status, product_condition):
            # TODO: Придумать как возвращать ошибку
            if DealerProductStausChange.objects.filter(
                dealer_product_id=dealer_product,
                status=CORRECT_CONDITIONS[0][0]
            ).exists():
                return
            DealerProductStausHistory.objects.create(
                dealer_product_id=dealer_product,
                status_type=product_status,
            )
            obj = DealerProductStausChange.objects.get(dealer_product_id=dealer_product)
            # TODO: разобраться почему статус сохраняется как: ('none',)
            obj.status = product_condition,
            obj.status_datetime = timezone.now()
            obj.save()

        if button == 'aside':
            _set_status_and_history(STATUS_TYPE[3][0], CORRECT_CONDITIONS[2][0])
        if button == 'disapprove':
            _set_status_and_history(STATUS_TYPE[4][0], CORRECT_CONDITIONS[1][0])
            obj_variants = DealerProductVariants.objects.filter(
                dealer_product_id=dealer_product
            )
            for obj_variant in obj_variants:
                obj_variant.delete()
        return

    # @swagger_auto_schema(responses={200: ProductSerializer})
    def post(self, request):
        """
        Метод сопоставления товара образцу (действие разметки)
        """
        params = request.POST
        dealer_product_id = force_int(params.get('dealer_product_id', 0))
        try:
            dealer_product = DealerPrice.objects.get(id=dealer_product_id)
        except DealerPrice.DoesNotExist:
            logger.warning('Запрашиваемый продукт диллера не найден')
            return JsonResponse(
                {},
                code=404,
                message='Запрашиваемый продукт диллера не найден'
            )
        button = params.get('button', '')
        if button == 'approve':
            is_manual = params.get('is_manual', '')
            if is_manual != 'True' and is_manual != 'False':
                logger.warning('Поступило неожиданное значение параметра is_manual')
                return JsonResponse(
                    {},
                    code=400,
                    message='Поступило неожиданное значение параметра is_manual'
                )
            try:
                self._set_approve(params, dealer_product, is_manual)
                return JsonResponse({}, message='Ок')
            except Exception as error:
                logger.error(f'Ошибка обработки запроса: {str(error)}')
        if button == 'aside' or button == 'disapprove':
            try:
                data = self._set_not_approve(button, dealer_product)
                print(data)
                if data:
                    return JsonResponse({}, code=400, message=data)
                return JsonResponse({}, message='Ок')
            except Exception as error:
                logger.error(f'Ошибка обработки запроса: {str(error)}')
        return JsonResponse(
                    {},
                    code=400,
                    message='Ошибка обработки запроса'
                )


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
