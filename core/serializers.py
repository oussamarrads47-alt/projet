"""
Serializers DRF pour TRANS-GEST.
"""
from rest_framework import serializers
from .models import Magasin, Detenteur, Materiel, Document, Mouvement


class MagasinSerializer(serializers.ModelSerializer):
    nombre_materiels = serializers.IntegerField(source='materiels.count', read_only=True)

    class Meta:
        model = Magasin
        fields = '__all__'


class DetenteurSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    nombre_materiels = serializers.IntegerField(source='materiels.count', read_only=True)

    class Meta:
        model = Detenteur
        fields = '__all__'


class MaterielSerializer(serializers.ModelSerializer):
    magasin_nom = serializers.CharField(source='magasin.nom', read_only=True)
    detenteur_nom = serializers.CharField(source='detenteur.__str__', read_only=True, default='—')
    type_display = serializers.CharField(source='get_type_materiel_display', read_only=True)
    etat_display = serializers.CharField(source='get_etat_display', read_only=True)

    class Meta:
        model = Materiel
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Document
        fields = '__all__'


class MouvementSerializer(serializers.ModelSerializer):
    materiel_designation = serializers.CharField(source='materiel.designation', read_only=True)
    document_type = serializers.CharField(source='document.type', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Mouvement
        fields = '__all__'
