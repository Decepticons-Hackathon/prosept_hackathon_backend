import logging
import time

from django.core.management.base import BaseCommand

from api.utils import MlMatches, force_int

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Обновление базы рекомендаций"

    def add_arguments(self, parser):
        parser.add_argument('--v', type=int, help='Вариант используемой ML модели')

    def handle(self, *args, **options):
        start = time.time()
        self.proccess(*args, **options)
        logger.info(f"Общее время выполнения: {time.time() - start}\n")

    def proccess(self, *args, **options):
        logger.info("Обновление базы рекомендаций")
        if options.get('v'):
            version = force_int(options.get('v'))
            MlMatches().get_ml_variants(version=version)
        else:
            MlMatches().get_ml_variants()
