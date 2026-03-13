"""
Tests pour les modèles de TRANS-GEST.
"""
from django.test import TestCase
from core.models import Magasin, Detenteur, Materiel, Document, Mouvement
from datetime import date


class MagasinModelTest(TestCase):
    def setUp(self):
        self.magasin = Magasin.objects.create(
            nom='Magasin Test', localisation='Rabat'
        )

    def test_str(self):
        self.assertEqual(str(self.magasin), 'Magasin Test')

    def test_get_absolute_url(self):
        self.assertEqual(self.magasin.get_absolute_url(), '/magasins/')

    def test_ordering(self):
        Magasin.objects.create(nom='AAA', localisation='Test')
        magasins = list(Magasin.objects.values_list('nom', flat=True))
        self.assertEqual(magasins, sorted(magasins))


class DetenteurModelTest(TestCase):
    def setUp(self):
        self.detenteur = Detenteur.objects.create(
            nom='BENALI Ahmed', grade='capitaine', fonction='Chef Section'
        )

    def test_str(self):
        self.assertEqual(str(self.detenteur), 'Capitaine BENALI Ahmed')

    def test_grade_choices(self):
        self.assertEqual(self.detenteur.get_grade_display(), 'Capitaine')


class MaterielModelTest(TestCase):
    def setUp(self):
        self.magasin = Magasin.objects.create(nom='Magasin 1', localisation='Test')
        self.detenteur = Detenteur.objects.create(
            nom='Test', grade='lieutenant', fonction='Test'
        )
        self.materiel = Materiel.objects.create(
            designation='Radio Test', type_materiel='radio',
            numero_serie='RT-001', etat='service',
            magasin=self.magasin, detenteur=self.detenteur,
        )

    def test_str(self):
        self.assertEqual(str(self.materiel), 'Radio Test (RT-001)')

    def test_etat_badge_class(self):
        self.assertEqual(self.materiel.etat_badge_class, 'badge-success')
        self.materiel.etat = 'hors_service'
        self.assertEqual(self.materiel.etat_badge_class, 'badge-danger')

    def test_unique_numero_serie(self):
        with self.assertRaises(Exception):
            Materiel.objects.create(
                designation='Duplicate', type_materiel='radio',
                numero_serie='RT-001', etat='service',
                magasin=self.magasin,
            )

    def test_detenteur_optional(self):
        m = Materiel.objects.create(
            designation='No Owner', type_materiel='radio',
            numero_serie='RT-002', etat='attente',
            magasin=self.magasin,
        )
        self.assertIsNone(m.detenteur)


class DocumentModelTest(TestCase):
    def setUp(self):
        self.document = Document.objects.create(
            type='50/4', date=date(2025, 3, 1),
            description='Test document',
        )

    def test_str(self):
        self.assertIn('50/4', str(self.document))

    def test_ordering(self):
        Document.objects.create(type='50/5', date=date(2025, 4, 1))
        docs = list(Document.objects.values_list('date', flat=True))
        self.assertEqual(docs, sorted(docs, reverse=True))


class MouvementModelTest(TestCase):
    def setUp(self):
        magasin = Magasin.objects.create(nom='Mag', localisation='Loc')
        self.materiel = Materiel.objects.create(
            designation='Radio M', type_materiel='radio',
            numero_serie='RM-001', etat='service', magasin=magasin,
        )
        self.document = Document.objects.create(
            type='50/4', date=date(2025, 3, 1),
        )
        self.mouvement = Mouvement.objects.create(
            type='entree', date=date(2025, 3, 1),
            materiel=self.materiel, document=self.document,
            quantite=2, observations='Test',
        )

    def test_str(self):
        self.assertIn('Entrée', str(self.mouvement))
        self.assertIn('Radio M', str(self.mouvement))

    def test_quantite_default(self):
        mv = Mouvement.objects.create(
            type='sortie', date=date(2025, 3, 2),
            materiel=self.materiel, document=self.document,
        )
        self.assertEqual(mv.quantite, 1)
