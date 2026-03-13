"""
Tests pour les vues Django de TRANS-GEST.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Magasin, Detenteur, Materiel, Document, Mouvement
from datetime import date


class ViewTestBase(TestCase):
    """Classe de base avec setup commun."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.magasin = Magasin.objects.create(nom='Mag1', localisation='Loc1')
        self.detenteur = Detenteur.objects.create(
            nom='Test', grade='lieutenant', fonction='Test'
        )
        self.materiel = Materiel.objects.create(
            designation='Radio Test', type_materiel='radio',
            numero_serie='RT-001', etat='service',
            magasin=self.magasin, detenteur=self.detenteur,
        )
        self.document = Document.objects.create(
            type='50/4', date=date(2025, 3, 1),
        )
        self.mouvement = Mouvement.objects.create(
            type='entree', date=date(2025, 3, 1),
            materiel=self.materiel, document=self.document,
        )


class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_login_page_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_redirect_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirect(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class DashboardViewTests(ViewTestBase):
    def test_dashboard_200(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_context(self):
        response = self.client.get(reverse('dashboard'))
        self.assertIn('stats', response.context)
        self.assertIn('materiels', response.context)


class MaterielViewTests(ViewTestBase):
    def test_list_200(self):
        response = self.client.get(reverse('materiel_list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_200(self):
        response = self.client.get(reverse('materiel_detail', args=[self.materiel.pk]))
        self.assertEqual(response.status_code, 200)

    def test_create_get(self):
        response = self.client.get(reverse('materiel_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(reverse('materiel_create'), {
            'designation': 'New', 'type_materiel': 'radio',
            'numero_serie': 'NEW-001', 'etat': 'service',
            'magasin': self.magasin.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Materiel.objects.filter(numero_serie='NEW-001').exists())

    def test_update_post(self):
        response = self.client.post(
            reverse('materiel_update', args=[self.materiel.pk]),
            {
                'designation': 'Updated', 'type_materiel': 'radio',
                'numero_serie': 'RT-001', 'etat': 'attente',
                'magasin': self.magasin.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.materiel.refresh_from_db()
        self.assertEqual(self.materiel.designation, 'Updated')

    def test_delete_post(self):
        response = self.client.post(reverse('materiel_delete', args=[self.materiel.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Materiel.objects.filter(pk=self.materiel.pk).exists())

    def test_filter_by_etat(self):
        response = self.client.get(reverse('materiel_list') + '?etat=service')
        self.assertEqual(response.status_code, 200)


class MagasinViewTests(ViewTestBase):
    def test_list_200(self):
        response = self.client.get(reverse('magasin_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(reverse('magasin_create'), {
            'nom': 'New Mag', 'localisation': 'Test',
        })
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        mag = Magasin.objects.create(nom='ToDelete', localisation='X')
        response = self.client.post(reverse('magasin_delete', args=[mag.pk]))
        self.assertEqual(response.status_code, 302)


class DetenteurViewTests(ViewTestBase):
    def test_list_200(self):
        response = self.client.get(reverse('detenteur_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(reverse('detenteur_create'), {
            'nom': 'New Det', 'grade': 'sergent', 'fonction': 'Test',
        })
        self.assertEqual(response.status_code, 302)


class DocumentViewTests(ViewTestBase):
    def test_list_200(self):
        response = self.client.get(reverse('document_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(reverse('document_create'), {
            'type': '50/5', 'date': '2025-04-01',
        })
        self.assertEqual(response.status_code, 302)


class MouvementViewTests(ViewTestBase):
    def test_list_200(self):
        response = self.client.get(reverse('mouvement_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(reverse('mouvement_create'), {
            'type': 'sortie', 'date': '2025-04-01',
            'materiel': self.materiel.pk,
            'document': self.document.pk,
            'quantite': 1,
        })
        self.assertEqual(response.status_code, 302)


class SearchViewTests(ViewTestBase):
    def test_search_200(self):
        response = self.client.get(reverse('search') + '?q=Radio')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.context)

    def test_search_empty(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
