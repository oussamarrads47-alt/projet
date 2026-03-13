"""
Statistiques de la base de donnees.
"""
from django.core.management.base import BaseCommand
from django.db.models import Count
from core.models import Magasin, Detenteur, Materiel, Document, Mouvement


class Command(BaseCommand):
    help = 'Affiche les statistiques detaillees de la base de donnees TRANS-GEST'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('[*] Statistiques TRANS-GEST'))
        self.stdout.write('')

        # General counts
        self.stdout.write(self.style.MIGRATE_HEADING('Resume general'))
        self.stdout.write(f'  Magasins     : {Magasin.objects.count()}')
        self.stdout.write(f'  Detenteurs   : {Detenteur.objects.count()}')
        self.stdout.write(f'  Materiels    : {Materiel.objects.count()}')
        self.stdout.write(f'  Documents    : {Document.objects.count()}')
        self.stdout.write(f'  Mouvements   : {Mouvement.objects.count()}')

        # Materiels by state
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Etat des materiels'))
        for entry in Materiel.objects.values('etat').annotate(c=Count('id')).order_by('-c'):
            label = dict(Materiel.ETAT_CHOICES).get(entry['etat'], entry['etat'])
            self.stdout.write(f'  {label}: {entry["c"]}')

        # Materiels by type
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Repartition par type'))
        for entry in Materiel.objects.values('type_materiel').annotate(c=Count('id')).order_by('-c'):
            label = dict(Materiel.TYPE_CHOICES).get(entry['type_materiel'], entry['type_materiel'])
            self.stdout.write(f'  {label}: {entry["c"]}')

        # Materiels per magasin
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Materiels par magasin'))
        for mag in Magasin.objects.annotate(c=Count('materiels')).order_by('-c'):
            self.stdout.write(f'  {mag.nom}: {mag.c}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('[OK] Statistiques terminees.'))
