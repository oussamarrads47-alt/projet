"""
API ViewSets DRF pour TRANS-GEST.
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Magasin, Detenteur, Materiel, Document, Mouvement
from .serializers import (
    MagasinSerializer, DetenteurSerializer, MaterielSerializer,
    DocumentSerializer, MouvementSerializer
)


class MagasinViewSet(viewsets.ModelViewSet):
    queryset = Magasin.objects.all()
    serializer_class = MagasinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'localisation']
    ordering_fields = ['nom', 'created_at']


class DetenteurViewSet(viewsets.ModelViewSet):
    queryset = Detenteur.objects.all()
    serializer_class = DetenteurSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'grade', 'fonction']
    ordering_fields = ['nom', 'grade', 'created_at']


class MaterielViewSet(viewsets.ModelViewSet):
    queryset = Materiel.objects.select_related('magasin', 'detenteur').all()
    serializer_class = MaterielSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['designation', 'numero_serie', 'type_materiel']
    ordering_fields = ['designation', 'etat', 'created_at']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'observations']
    ordering_fields = ['date', 'type', 'created_at']


class MouvementViewSet(viewsets.ModelViewSet):
    queryset = Mouvement.objects.select_related('materiel', 'document').all()
    serializer_class = MouvementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['materiel__designation', 'observations']
    ordering_fields = ['date', 'type', 'created_at']
