"""
Formulaires Django pour TRANS-GEST.
"""
from django import forms
from .models import Magasin, Detenteur, Materiel, Document, Mouvement


class DateInput(forms.DateInput):
    """Widget date HTML5."""
    input_type = 'date'


class MagasinForm(forms.ModelForm):
    """Formulaire pour les magasins."""
    class Meta:
        model = Magasin
        fields = ['nom', 'localisation']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du magasin',
            }),
            'localisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse / Localisation',
            }),
        }


class DetenteurForm(forms.ModelForm):
    """Formulaire pour les détenteurs."""
    class Meta:
        model = Detenteur
        fields = ['nom', 'grade', 'fonction', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du détenteur',
            }),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'fonction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fonction / Rôle',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class MaterielForm(forms.ModelForm):
    """Formulaire pour les matériels."""
    class Meta:
        model = Materiel
        fields = [
            'designation', 'type_materiel', 'numero_serie', 'etat',
            'magasin', 'detenteur', 'image', 'date_entree', 'date_sortie', 'date_retour',
        ]
        widgets = {
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Désignation du matériel',
            }),
            'type_materiel': forms.Select(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de série unique',
            }),
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'magasin': forms.Select(attrs={'class': 'form-control'}),
            'detenteur': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'date_entree': DateInput(attrs={'class': 'form-control'}),
            'date_sortie': DateInput(attrs={'class': 'form-control'}),
            'date_retour': DateInput(attrs={'class': 'form-control'}),
        }


class DocumentForm(forms.ModelForm):
    """Formulaire pour les documents."""
    class Meta:
        model = Document
        fields = ['type', 'date', 'description', 'date_entree', 'date_sortie', 'date_retour', 'observations']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du document',
            }),
            'date_entree': DateInput(attrs={'class': 'form-control'}),
            'date_sortie': DateInput(attrs={'class': 'form-control'}),
            'date_retour': DateInput(attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observations',
            }),
        }


class MouvementForm(forms.ModelForm):
    """Formulaire pour les mouvements."""
    class Meta:
        model = Mouvement
        fields = ['type', 'date', 'materiel', 'document', 'quantite', 'observations']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control'}),
            'materiel': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Quantité',
            }),
            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observations',
            }),
        }
