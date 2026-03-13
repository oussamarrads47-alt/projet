"""
Tests pour les formulaires Django de TRANS-GEST.
"""
from django.test import TestCase
from core.forms import MagasinForm, DetenteurForm, MaterielForm, DocumentForm, MouvementForm
from core.models import Magasin, Detenteur, Materiel, Document
from datetime import date


class MagasinFormTest(TestCase):
    def test_valid(self):
        form = MagasinForm(data={'nom': 'Test', 'localisation': 'Loc'})
        self.assertTrue(form.is_valid())

    def test_missing_nom(self):
        form = MagasinForm(data={'localisation': 'Loc'})
        self.assertFalse(form.is_valid())
        self.assertIn('nom', form.errors)


class DetenteurFormTest(TestCase):
    def test_valid(self):
        form = DetenteurForm(data={
            'nom': 'Test', 'grade': 'lieutenant', 'fonction': 'Chef'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_grade(self):
        form = DetenteurForm(data={
            'nom': 'Test', 'grade': 'invalid', 'fonction': 'Chef'
        })
        self.assertFalse(form.is_valid())


class MaterielFormTest(TestCase):
    def setUp(self):
        self.magasin = Magasin.objects.create(nom='Mag', localisation='Loc')

    def test_valid(self):
        form = MaterielForm(data={
            'designation': 'Radio', 'type_materiel': 'radio',
            'numero_serie': 'RS-001', 'etat': 'service',
            'magasin': self.magasin.pk,
        })
        self.assertTrue(form.is_valid())

    def test_missing_required(self):
        form = MaterielForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('designation', form.errors)
        self.assertIn('numero_serie', form.errors)
        self.assertIn('magasin', form.errors)


class DocumentFormTest(TestCase):
    def test_valid(self):
        form = DocumentForm(data={
            'type': '50/4', 'date': '2025-03-01',
        })
        self.assertTrue(form.is_valid())

    def test_missing_date(self):
        form = DocumentForm(data={'type': '50/4'})
        self.assertFalse(form.is_valid())


class MouvementFormTest(TestCase):
    def setUp(self):
        magasin = Magasin.objects.create(nom='Mag', localisation='Loc')
        self.materiel = Materiel.objects.create(
            designation='Radio', type_materiel='radio',
            numero_serie='RS-001', etat='service', magasin=magasin,
        )
        self.document = Document.objects.create(
            type='50/4', date=date(2025, 3, 1),
        )

    def test_valid(self):
        form = MouvementForm(data={
            'type': 'entree', 'date': '2025-03-01',
            'materiel': self.materiel.pk,
            'document': self.document.pk,
            'quantite': 1,
        })
        self.assertTrue(form.is_valid())

    def test_missing_materiel(self):
        form = MouvementForm(data={
            'type': 'entree', 'date': '2025-03-01',
            'document': self.document.pk, 'quantite': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('materiel', form.errors)
