import csv
import logging
import os

from django.conf import settings
from django.db.models import Subquery
from django.http import JsonResponse as JsonResponseBase
from rest_framework import status

from api import __version__ as version
from api.models import (CORRECT_CONDITIONS, STATUS_TYPE, Dealer, DealerPrice,
                        DealerProduct, DealerProductStausChange,
                        DealerProductStausHistory, DealerProductVariants,
                        Product)
from api.serializers.ml_serializers import (DealerProductMlSerializer,
                                            ProductMlSerializer)
from ml_models.decepticon_ml_model.recommendation_model import \
    recommendation_model

logger = logging.getLogger(__name__)


class JsonResponse(JsonResponseBase):
    """
    Метод ответа в формате JSON с версией приложения
    """
    def __init__(
            self, data, code=status.HTTP_200_OK, message='', *args, **kwargs):
        _ = {
            'code': code,
            'message': message,
            'version': version,
            'data': data
        }
        super().__init__(_, *args, **kwargs)


def force_int(value, default=0):
    """
    Безопасное приведение к int
    """
    try:
        return int(value)
    except Exception:
        return default


def force_float(value, default=0.):
    """
    Безопасное приведение к float
    """
    try:
        return float(value)
    except Exception:
        return default


class CsvParser:
    """
    Класс импорта данных из cvs файлов
    """
    def __parse_folder(self):
        files_list = {}
        try:
            for _, _, files in os.walk(settings.MEDIA_ROOT):
                for file in files:
                    file_path = os.path.join(settings.MEDIA_ROOT, file)
                    files_list[file.split('.')[0]] = file_path
        except Exception as error:
            logger.warning(f'Ошибка считывания файлов: {error}')
        return files_list

    def __save_dealer_model(self, line):
        try:
            Dealer.objects.get_or_create(
                id=force_int(line[0]),
                name=line[1]
            )
        except Exception as error:
            logger.warning(f'Ошибка добавления данных Dealer: {error}')
        return

    def __save_product_model(self, line):
        try:
            dict_data = {
                'product_id': line[1],
                'article': line[2],
                'ean_13': line[3],
                'name': line[4],
                'cost': force_float(line[5]),
                # 'min_rec_price': force_float(line[6]),
                'rec_price': force_float(line[6]),
                'category_id': force_float(line[7]),
                'ozon_name': line[8],
                'name_1c': line[9],
                'wb_name': line[10],
                'ozon_article': line[11],
                'wb_article': line[12],
                'ym_article': line[13],
            }
            Product.objects.get_or_create(**dict_data)
        except Exception as error:
            logger.warning(f'Ошибка добавления данных Product: {error}')
        return

    def __save_dealer_price_model(self, line):
        try:
            dealer = Dealer.objects.get(id=force_int(line[6]))
            dict_data = {
                'product_key': line[1],
                'price': force_float(line[2]),
                'product_url': line[3],
                'product_name': line[4],
                'date': line[5],
                'dealer': dealer
            }
            obj, _ = DealerPrice.objects.get_or_create(**dict_data)
            dict_status_data = {
                'dealer_product_id': obj,
                'dealer_id': dealer,
            }
            dict_history_data = {
                'dealer_product_id': obj
            }
            DealerProductStausChange.objects.get_or_create(**dict_status_data)
            DealerProductStausHistory.objects.get_or_create(**dict_history_data)
        except Exception as error:
            logger.warning(f'Ошибка добавления данных DealerPrice: {error}')
        return

    def __save_dealer_product_model(self, line):
        try:
            dealer = Dealer.objects.get(id=force_int(line[2]))
            product = Product.objects.get(product_id=force_int(line[3]))
            dict_data = {
                'product_id': product,
                'dealer_id': dealer
            }
            obj, _ = DealerProduct.objects.get_or_create(**dict_data)
            prices = DealerPrice.objects.filter(product_key=line[1])
            for price in prices:
                obj.key.add(price)
            obj.save()
        except Exception as error:
            logger.warning(
                f'Ошибка добавления данных DealerProduct: {error}'
            )
        return

    def __save_data(self, files):
        if 'marketing_dealer' in files:
            with open(
                files['marketing_dealer'], 'r', newline=''
            ) as csvfile:
                linereader = csv.reader(csvfile, delimiter=';')
                for row in linereader:
                    if 'id' not in row[0]:
                        self.__save_dealer_model(row)
        if 'marketing_product' in files:
            with open(
                files['marketing_product'], 'r', newline=''
            ) as csvfile:
                linereader = csv.reader(csvfile, delimiter=';')
                for row in linereader:
                    if 'id' not in row[1]:
                        self.__save_product_model(row)
        if 'marketing_dealerprice' in files:
            with open(
                files['marketing_dealerprice'], 'r', newline=''
            ) as csvfile:
                linereader = csv.reader(csvfile, delimiter=';')
                for row in linereader:
                    if 'id' not in row[0]:
                        self.__save_dealer_price_model(row)
        if 'marketing_productdealerkey' in files:
            with open(
                files['marketing_productdealerkey'], 'r', newline=''
            ) as csvfile:
                linereader = csv.reader(csvfile, delimiter=';')
                for row in linereader:
                    if 'id' not in row[0]:
                        self.__save_dealer_product_model(row)

    def get_data(self):
        files = self.__parse_folder()
        self.__save_data(files)


def set_status_change():
    """
    Первичное наполнение истории и статусов продуктов диллера
    """
    products_matched = DealerProduct.objects.all()
    products = DealerPrice.objects.filter(
        id__in=Subquery(products_matched.values('key'))
    )
    for product in products:
        p_match = DealerProduct.objects.get(key=product)
        p_status = DealerProductStausChange.objects.get(
            dealer_product_id=product
        )
        p_status.status = CORRECT_CONDITIONS[0][0]
        p_status.product_id = p_match.product_id
        p_status.save()
        DealerProductStausHistory.objects.create(
            dealer_product_id=product,
            status_type=STATUS_TYPE[1][0]
        )


class MlMatches:
    """
    Класс для взаимодействия с ML моделями
    """
    def __get_diller_data_to_matches(self):
        diller_products = DealerProductStausChange.objects.filter(
            status=CORRECT_CONDITIONS[2][0]
        )
        data = DealerProductMlSerializer(diller_products, many=True).data
        return [dict(item) for item in data]

    def __get_products_data(self):
        products = Product.objects.all().order_by('id')
        data = ProductMlSerializer(products, many=True).data
        return [dict(item) for item in data]

    def __set_variants_to_db(self, items):
        logger.info('Стираю старые данные вариантов.')
        try:
            DealerProductVariants.objects.all().delete()
        except Exception as error:
            logger.error(f'Ошибка удаления старых данных вариантов: {str(error)}')
            return
        logger.info('Начинаю запись вариантов в БД.')
        for item in items:
            if len(item.get('variants')) == 0:
                continue
            dict_for_db = {}
            try:
                dealer_product = DealerPrice.objects.get(id=item.get('dealer_product_id'))
                dict_for_db['dealer_product_id'] = dealer_product
                dict_for_db['dealer_id'] = dealer_product.dealer
            except DealerPrice.DoesNotExist as error:
                logger.warning(f'Ошибка получения объекта DealerPrice: {str(error)}')
                continue
            for id in item.get('variants'):
                try:
                    product = Product.objects.get(id=id)
                    dict_for_db['product_id'] = product
                    dict_for_db['degree_of_agreement'] = item.get('variants').index(id) + 1
                except Product.DoesNotExist as error:
                    logger.warning(f'Ошибка получения объекта Product: {str(error)}')
                    continue
                DealerProductVariants.objects.create(**dict_for_db)
        logger.info('Завершена запись вариантов в БД.')
        return

    def get_ml_variants(self):
        variants_list = []
        try:
            products_data = self.__get_products_data()
            data_for_matching = self.__get_diller_data_to_matches()
        except Exception as error:
            logger.error(f'Ошибка получения объектов для обработки: {str(error)}')
            return
        cnt = 0
        logger.info(f'Начинаю обработку {len(data_for_matching)} позиций.')
        for item in data_for_matching:
            list_for_model = [
                {
                    'product_name': item.get('product_name'),
                    'dealer_id': item.get('dealer_id')
                }
            ]
            try:
                data = recommendation_model(list_for_model, products_data)
                dict_for_base = {
                    'dealer_product_id': item.get('dealer_product_id'),
                    'variants': data
                }
                variants_list.append(dict_for_base)
            except Exception as error:
                logger.error(f'Ошибка получения вариантов для объекта {item}: {str(error)}')
            cnt += 1
        logger.info(f'Получение вариантов для {cnt} записей товаров завершено.')
        try:
            self.__set_variants_to_db(variants_list)
        except Exception as error:
            logger.error(f'Ошибка сохранения результатов в БД: {str(error)}')
        return
