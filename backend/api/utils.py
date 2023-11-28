import csv
import logging
import os

from django.http import JsonResponse as JsonResponseBase
from django.conf import settings
from rest_framework import status

from api import __version__ as version
from api.models import Dealer, Product, DealerPrice, DealerProduct


logger = logging.getLogger(__name__)

class JsonResponse(JsonResponseBase):
    """
    Метод ответа в формате JSON с версией приложения
    """
    def __init__(
            self, data, code=status.HTTP_200_OK, message='', *args, **kwargs
        ):
        _ = {
            'code': code,
            'message': message,
            'version': version,
            'data': data
        }
        super().__init__(_, *args, **kwargs)


def force_int(value, default=0):
    '''
    Безопасное приведение к int
    '''
    try:
        return int(value)
    except:
        return default


def force_float(value, default=0.):
    '''
    Безопасное приведение к float
    '''
    try:
        return float(value)
    except:
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
            DealerPrice.objects.get_or_create(**dict_data)
        except Exception as error:
            logger.warning(f'Ошибка добавления данных DealerPrice: {error}')
        return

    def __save_dealer_product_model(self, line):
        try:
            dealer = Dealer.objects.get(id=force_int(line[2]))
            product = Product.objects.get(id=force_int(line[3]))
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


class Matches:
    """
    Класс для взаимодействия с DS
    """
    def get(self):
        ...