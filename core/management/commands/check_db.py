"""
Commande de verification de la base de donnees.
"""
from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Magasin, Detenteur, Materiel, Document, Mouvement


class Command(BaseCommand):
    help = 'Verifie la connexion et l\'etat de la base de donnees TRANS-GEST'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('[*] Verification de la base de donnees TRANS-GEST'))
        self.stdout.write('')

        # Check connection
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('[OK] Connexion a la base de donnees : OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'[ERREUR] Connexion echouee : {e}'))
            return

        # Check tables
        tables = connection.introspection.table_names()
        expected = ['core_magasin', 'core_detenteur', 'core_materiel', 'core_document', 'core_mouvement']
        for table in expected:
            if table in tables:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Table {table} : presente'))
            else:
                self.stdout.write(self.style.WARNING(f'  [!] Table {table} : absente'))

        # Record counts
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('[*] Comptage des enregistrements'))
        models = [
            ('Magasins', Magasin),
            ('Detenteurs', Detenteur),
            ('Materiels', Materiel),
            ('Documents', Document),
            ('Mouvements', Mouvement),
        ]
        for name, model in models:
            count = model.objects.count()
            self.stdout.write(f'  {name}: {count}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('[OK] Verification terminee.'))
