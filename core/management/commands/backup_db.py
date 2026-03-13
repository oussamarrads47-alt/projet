"""
Commande de sauvegarde de la base de donnees SQLite.
"""
import shutil
import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Cree une sauvegarde de la base de donnees SQLite'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir', type=str, default='backups',
            help='Repertoire de destination des sauvegardes (par defaut: backups/)',
        )

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default'].get('NAME')
        if not db_path or not Path(db_path).exists():
            self.stdout.write(self.style.ERROR('[ERREUR] Fichier de base de donnees introuvable.'))
            return

        output_dir = Path(settings.BASE_DIR) / options['output_dir']
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'transgest_backup_{timestamp}.sqlite3'
        backup_path = output_dir / backup_name

        try:
            shutil.copy2(db_path, backup_path)
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            self.stdout.write(self.style.SUCCESS(
                f'[OK] Sauvegarde creee : {backup_path} ({size_mb:.2f} Mo)'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'[ERREUR] Erreur lors de la sauvegarde : {e}'))
