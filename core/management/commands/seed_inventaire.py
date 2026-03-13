"""
Commande Django pour préremplir la base de données avec les données
du tableau logistique militaire (matériels radio et radar).

Usage:
    python manage.py seed_inventaire
    python manage.py seed_inventaire --reset    # supprimer et recréer
"""
from django.core.management.base import BaseCommand
from core.models import CategorieMaterielLogistique, LigneInventaireLogistique


# ──────────────────────────────────────────────────────────────────────────────
# Données du catalogue logistique
# ──────────────────────────────────────────────────────────────────────────────
CATALOGUE = [
    {
        'code': 'radar',
        'ordre': 1,
        'materiels': [
            'RADAR BOR-A 550A',
            'RADAR BOR-A 560',
            'RADAR GO 12',
            'RADAR DE SURVEILLANCE ARSS1',
            'CABLE DE 50 M POUR RADAR ARSS1',
            'CASQUE MANHATAINE M 80',
        ],
    },
    {
        'code': 'uhf',
        'ordre': 2,
        'materiels': [
            'E/R AN/URC-200',
            'STATION V/UHF MT-3100 /50W MULTIBAND',
            'STATION V/UHF MT-3100 /7W MULTIBAND',
            'STATION FHN NERA TERMINALE INTERLINK',
            'STATION FHN NERA CITYLINK',
            'EQUIPEMENT FHNT STATION DE BASE',
            'EQUIPEMENT FHNT RELAIS',
            'EQUIPEMENT FHNT NMS',
        ],
    },
    {
        'code': 'vhf_groupe',
        'ordre': 3,
        'materiels': [
            'E/R TRC-5103',
            'E/R KENWOOD TK-2170',
            'E/R KENWOOD TK-259',
            'E/R KENWOOD TK-270',
            'E/R KENWOOD TK-2107',
            'E/R KENWOOD TK-2140',
            'E/R MOTOROLA DP-3400',
            'E/R MOTOROLA DP-3401',
            'E/R MOTOROLA DP-3600',
            'E/R MOTOROLA DP-4400',
            'REPETEUR MOTOROLA DR 3000 A50',
            'REPETEUR MOTOROLA SLR 5500',
        ],
    },
    {
        'code': 'vhf_cie',
        'ordre': 4,
        'materiels': [
            'E/R AN/VRC 90B',
            'E/R AN/PRC 119E',
            'E/R AN/VRC 90E',
            'E/R AN/VRC 88 E GPS',
            'IK SINGLE RADIO WHEELED MODE RAT (RACK POUR AN/VRC88)',
            'E/R PRC 1077 /50W',
            'E/R PRC 1077 /5W',
            'E/R PRC 2189 /50W',
            'E/R PRC 2189 /10W',
            'STATION DE BASE TK-7160 (KENWOOD)',
            'STATION DE BASE FIXE DM-3600 (MOTOROLA)',
            'STATION DE BASE MOBILE DM-3600 (MOTOROLA)',
        ],
    },
    {
        'code': 'hf',
        'ordre': 5,
        'materiels': [
            'E/R TRC 372 /20W',
            'E/R PRC 1099 HF /100W',
            'E/R TRC 340 /20W',
            'E/R TRC 3600 /20W',
            'E/R TRC 3700 /125W',
            'E/R CODAN 2110',
            'STATION CODAN SENTRY FIXE 2310',
            'STATION CODAN SENTRY MOBILE 3046',
        ],
    },
]


class Command(BaseCommand):
    help = 'Prérempli les données de l\'inventaire logistique militaire.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprime les données existantes avant d\'insérer.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            LigneInventaireLogistique.objects.all().delete()
            CategorieMaterielLogistique.objects.all().delete()
            self.stdout.write(self.style.WARNING('Données existantes supprimées.'))

        created_cats = 0
        created_lignes = 0

        for bloc in CATALOGUE:
            cat, cat_created = CategorieMaterielLogistique.objects.get_or_create(
                code=bloc['code'],
                defaults={'ordre': bloc['ordre']},
            )
            if cat_created:
                created_cats += 1
                self.stdout.write(f'  + Catégorie créée : {cat}')
            else:
                # Mettre à jour l'ordre si nécessaire
                if cat.ordre != bloc['ordre']:
                    cat.ordre = bloc['ordre']
                    cat.save(update_fields=['ordre'])

            for i, designation in enumerate(bloc['materiels'], start=1):
                # Utilise get_or_create pour éviter les doublons
                # Les valeurs numériques sont toutes à 0 par défaut
                ligne, ligne_created = LigneInventaireLogistique.objects.get_or_create(
                    categorie=cat,
                    designation=designation,
                    defaults={
                        'ordre': i,
                        'qte': 0, 'svc': 0, 'mag': 0, 'rep': 0,
                        'gmi': 0, 'gs':  0, 'gcs': 0,
                    },
                )
                if ligne_created:
                    created_lignes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nTermine : {created_cats} categorie(s), {created_lignes} ligne(s) creee(s).\n'
                f'  Mettez a jour les quantites via /admin/ > Lignes Inventaire Logistique.'
            )
        )
