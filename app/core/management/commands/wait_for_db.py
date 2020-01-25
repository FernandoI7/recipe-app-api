import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Comando do Django para pausar a execução até o BD estar pronto"""

    def handle(self, *args, **kwargs):
        self.stdout.write('Aguandando o BD...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('BD indisponível, esperando 1 segundo...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('BD disponível!'))