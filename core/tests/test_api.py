"""
Tests pour l'API REST de TRANS-GEST.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Magasin, Detenteur, Materiel, Document, Mouvement
from datetime import date


class APIAuthMixin:
    """Mixin pour l'authentification des tests API."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testapi', password='testpass123'
        )
        self.client.force_authenticate(user=self.user)


class MagasinAPITest(APIAuthMixin, TestCase):
    """Tests API pour le modèle Magasin."""

    def setUp(self):
        super().setUp()
        self.magasin = Magasin.objects.create(
            nom='Magasin Test API', localisation='Rabat'
        )
        self.url = '/api/magasins/'

    def test_list_magasins(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_magasin(self):
        data = {'nom': 'Nouveau Magasin', 'localisation': 'Casablanca'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Magasin.objects.count(), 2)

    def test_retrieve_magasin(self):
        response = self.client.get(f'{self.url}{self.magasin.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nom'], 'Magasin Test API')

    def test_update_magasin(self):
        data = {'nom': 'Magasin Modifié', 'localisation': 'Tanger'}
        response = self.client.put(f'{self.url}{self.magasin.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.magasin.refresh_from_db()
        self.assertEqual(self.magasin.nom, 'Magasin Modifié')

    def test_delete_magasin(self):
        response = self.client.delete(f'{self.url}{self.magasin.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Magasin.objects.count(), 0)

    def test_search_magasin(self):
        response = self.client.get(f'{self.url}?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DetenteurAPITest(APIAuthMixin, TestCase):
    """Tests API pour le modèle Detenteur."""

    def setUp(self):
        super().setUp()
        self.detenteur = Detenteur.objects.create(
            nom='Détenteur Test', grade='capitaine',
            fonction='Chef de section'
        )
        self.url = '/api/detenteurs/'

    def test_list_detenteurs(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_detenteur(self):
        data = {
            'nom': 'Nouveau Détenteur',
            'grade': 'lieutenant',
            'fonction': 'Adjoint'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_detenteur(self):
        response = self.client.get(f'{self.url}{self.detenteur.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_detenteur(self):
        data = {
            'nom': 'Détenteur Modifié',
            'grade': 'commandant',
            'fonction': 'Chef de bureau'
        }
        response = self.client.put(f'{self.url}{self.detenteur.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_detenteur(self):
        response = self.client.delete(f'{self.url}{self.detenteur.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MaterielAPITest(APIAuthMixin, TestCase):
    """Tests API pour le modèle Materiel."""

    def setUp(self):
        super().setUp()
        self.magasin = Magasin.objects.create(
            nom='Magasin Central', localisation='Rabat'
        )
        self.materiel = Materiel.objects.create(
            designation='Radio Test',
            type_materiel='radio',
            numero_serie='API-TEST-001',
            etat='service',
            magasin=self.magasin
        )
        self.url = '/api/materiels/'

    def test_list_materiels(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_materiel(self):
        data = {
            'designation': 'Nouveau Matériel',
            'type_materiel': 'informatique',
            'numero_serie': 'API-TEST-002',
            'etat': 'service',
            'magasin': self.magasin.pk
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_materiel(self):
        response = self.client.get(f'{self.url}{self.materiel.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('magasin_nom', response.data)

    def test_update_materiel(self):
        data = {
            'designation': 'Radio Modifiée',
            'type_materiel': 'radio',
            'numero_serie': 'API-TEST-001',
            'etat': 'attente',
            'magasin': self.magasin.pk
        }
        response = self.client.put(f'{self.url}{self.materiel.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_materiel(self):
        response = self.client.delete(f'{self.url}{self.materiel.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_materiel(self):
        response = self.client.get(f'{self.url}?search=Radio')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unique_numero_serie(self):
        data = {
            'designation': 'Doublon',
            'type_materiel': 'radio',
            'numero_serie': 'API-TEST-001',
            'etat': 'service',
            'magasin': self.magasin.pk
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DocumentAPITest(APIAuthMixin, TestCase):
    """Tests API pour le modèle Document."""

    def setUp(self):
        super().setUp()
        self.document = Document.objects.create(
            type='50/4', date=date(2024, 1, 15),
            description='Document de test API'
        )
        self.url = '/api/documents/'

    def test_list_documents(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_document(self):
        data = {
            'type': '50/5',
            'date': '2024-02-01',
            'description': 'Nouveau document'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_document(self):
        response = self.client.get(f'{self.url}{self.document.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_document(self):
        response = self.client.delete(f'{self.url}{self.document.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MouvementAPITest(APIAuthMixin, TestCase):
    """Tests API pour le modèle Mouvement."""

    def setUp(self):
        super().setUp()
        self.magasin = Magasin.objects.create(
            nom='Magasin Mvt', localisation='Rabat'
        )
        self.materiel = Materiel.objects.create(
            designation='Matériel Mvt',
            type_materiel='radio',
            numero_serie='MVT-API-001',
            etat='service',
            magasin=self.magasin
        )
        self.document = Document.objects.create(
            type='50/4', date=date(2024, 1, 15)
        )
        self.mouvement = Mouvement.objects.create(
            type='entree', date=date(2024, 1, 15),
            materiel=self.materiel, document=self.document,
            quantite=1
        )
        self.url = '/api/mouvements/'

    def test_list_mouvements(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_mouvement(self):
        data = {
            'type': 'sortie',
            'date': '2024-02-01',
            'materiel': self.materiel.pk,
            'document': self.document.pk,
            'quantite': 2
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_mouvement(self):
        response = self.client.get(f'{self.url}{self.mouvement.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('materiel_designation', response.data)

    def test_delete_mouvement(self):
        response = self.client.delete(f'{self.url}{self.mouvement.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
