"""
URL patterns pour l'API REST de TRANS-GEST.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    MagasinViewSet, DetenteurViewSet, MaterielViewSet,
    DocumentViewSet, MouvementViewSet
)

router = DefaultRouter()
router.register(r'magasins', MagasinViewSet)
router.register(r'detenteurs', DetenteurViewSet)
router.register(r'materiels', MaterielViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'mouvements', MouvementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
