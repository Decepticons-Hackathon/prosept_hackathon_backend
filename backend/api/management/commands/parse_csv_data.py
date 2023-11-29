import logging
import time

from django.core.management.base import BaseCommand

from api.utils import CsvParser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Импорт данных из cvs файлов'

    def handle(self, *args, **options):
        start = time.time()
        self.proccess(*args, **options)
        logger.info(f'Общее время выполнения: {time.time() - start}\n')

    def proccess(self, *args, **options):
        logger.info('Обработка данных с csv файлов')
        CsvParser().get_data()
