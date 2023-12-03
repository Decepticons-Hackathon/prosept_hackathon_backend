import logging
import time

from django.core.management.base import BaseCommand

from api.utils import MlMatches

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Обновление базы рекомендаций"

    def handle(self, *args, **options):
        start = time.time()
        self.proccess(*args, **options)
        logger.info(f"Общее время выполнения: {time.time() - start}\n")

    def proccess(self, *args, **options):
        logger.info("Обновление базы рекомендаций")
        MlMatches().get_ml_variants()
