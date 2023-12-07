import logging
import time

from django.core.management.base import BaseCommand

from api.utils import set_status_change

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Наполнение статусов и истории продуктов диллера'

    def handle(self, *args, **options):
        start = time.time()
        self.proccess(*args, **options)
        logger.info(f'Общее время выполнения: {time.time() - start}')

    def proccess(self, *args, **options):
        logger.info(
            'Первичное наполнение истории и статусов продуктов диллера'
        )
        set_status_change()
