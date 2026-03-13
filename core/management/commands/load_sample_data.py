"""
Charge les données d'exemple dans la base de données.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Charge toutes les donnees d\'exemple (fixtures) dans la base de donnees'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Supprimer les donnees existantes avant de charger',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('[*] Chargement des donnees d\'exemple TRANS-GEST'))

        if options['reset']:
            self.stdout.write(self.style.WARNING('[!] Suppression des donnees existantes...'))
            from core.models import Mouvement, Document, Materiel, Detenteur, Magasin
            Mouvement.objects.all().delete()
            Document.objects.all().delete()
            Materiel.objects.all().delete()
            Detenteur.objects.all().delete()
            Magasin.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('  [OK] Donnees supprimees.'))

        fixtures = [
            'fixtures/magasins.json',
            'fixtures/detenteurs.json',
            'fixtures/materiels.json',
            'fixtures/documents.json',
            'fixtures/mouvements.json',
        ]

        for fixture in fixtures:
            self.stdout.write(f'  Chargement de {fixture}...')
            try:
                call_command('loaddata', fixture, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'    [OK] {fixture} charge'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'    [ERREUR] {e}'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('[OK] Toutes les donnees d\'exemple ont ete chargees !'))
