"""
Modèles de données pour TRANS-GEST.
Système de Gestion des Matériels de Transmission
"""
from django.db import models
from django.urls import reverse


class Magasin(models.Model):
    """Modèle représentant un magasin/entrepôt."""
    nom = models.CharField('Nom du magasin', max_length=200)
    localisation = models.CharField('Localisation', max_length=300)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        db_table = 'core_magasin'
        verbose_name = 'Magasin'
        verbose_name_plural = 'Magasins'
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('magasin_list')


class Detenteur(models.Model):
    """Modèle représentant un détenteur/unité opérationnelle."""
    GRADE_CHOICES = [
        ('soldat', 'Soldat'),
        ('caporal', 'Caporal'),
        ('sergent', 'Sergent'),
        ('adjudant', 'Adjudant'),
        ('lieutenant', 'Lieutenant'),
        ('capitaine', 'Capitaine'),
        ('commandant', 'Commandant'),
        ('colonel', 'Colonel'),
        ('general', 'Général'),
    ]

    nom = models.CharField('Nom', max_length=200)
    grade = models.CharField('Grade', max_length=100, choices=GRADE_CHOICES, default='lieutenant')
    fonction = models.CharField('Fonction', max_length=200)
    image = models.ImageField('Photo', upload_to='detenteurs/', null=True, blank=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        db_table = 'core_detenteur'
        verbose_name = 'Détenteur'
        verbose_name_plural = 'Détenteurs'
        ordering = ['nom']

    def __str__(self):
        return f"{self.get_grade_display()} {self.nom}"

    def get_absolute_url(self):
        return reverse('detenteur_list')


class Materiel(models.Model):
    """Modèle représentant un matériel de transmission."""
    TYPE_CHOICES = [
        ('radio', 'Radio'),
        ('telephonique', 'Téléphonique'),
        ('informatique', 'Informatique'),
        ('vehicule', 'Véhicule'),
        ('armement', 'Armement'),
        ('optique', 'Optique'),
        ('autre', 'Autre'),
    ]
    ETAT_CHOICES = [
        ('service', 'En Service'),
        ('attente', 'En Attente'),
        ('approvisionnement', 'Approvisionnement'),
        ('hors_service', 'Hors Service'),
    ]

    designation = models.CharField('Désignation', max_length=300)
    type_materiel = models.CharField('Type', max_length=100, choices=TYPE_CHOICES, default='radio')
    numero_serie = models.CharField('Numéro de série', max_length=100, unique=True)
    etat = models.CharField('État', max_length=50, choices=ETAT_CHOICES, default='service')
    magasin = models.ForeignKey(
        Magasin, on_delete=models.CASCADE,
        related_name='materiels', verbose_name='Magasin'
    )
    detenteur = models.ForeignKey(
        Detenteur, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='materiels', verbose_name='Détenteur'
    )
    image = models.ImageField('Photo', upload_to='materiels/', null=True, blank=True)
    date_entree = models.DateField('Date d\'entrée', null=True, blank=True)
    date_sortie = models.DateField('Date de sortie', null=True, blank=True)
    date_retour = models.DateField('Date de retour', null=True, blank=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        db_table = 'core_materiel'
        verbose_name = 'Matériel'
        verbose_name_plural = 'Matériels'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['numero_serie']),
            models.Index(fields=['etat']),
            models.Index(fields=['type_materiel']),
            models.Index(fields=['magasin', 'etat']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.designation} ({self.numero_serie})"

    def get_absolute_url(self):
        return reverse('materiel_detail', kwargs={'pk': self.pk})

    @property
    def etat_badge_class(self):
        """Retourne la classe CSS pour le badge d'état."""
        classes = {
            'service': 'badge-success',
            'attente': 'badge-warning',
            'approvisionnement': 'badge-info',
            'hors_service': 'badge-danger',
        }
        return classes.get(self.etat, 'badge-secondary')


class Document(models.Model):
    """Modèle représentant un document de gestion."""
    TYPE_CHOICES = [
        ('50/4', '50/4'),
        ('50/5', '50/5'),
        ('50/6', '50/6'),
        ('50/7', '50/7'),
        ('50/8', '50/8'),
        ('autre', 'Autre'),
    ]

    type = models.CharField('Type de document', max_length=50, choices=TYPE_CHOICES, default='50/4')
    date = models.DateField('Date du document')
    description = models.TextField('Description', blank=True)
    date_entree = models.DateField('Date d\'entrée', null=True, blank=True)
    date_sortie = models.DateField('Date de sortie', null=True, blank=True)
    date_retour = models.DateField('Date de retour', null=True, blank=True)
    observations = models.TextField('Observations', blank=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        db_table = 'core_document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-date']

    def __str__(self):
        return f"Document {self.type} - {self.date.strftime('%d/%m/%Y') if self.date else 'N/A'}"

    def get_absolute_url(self):
        return reverse('document_list')


class Mouvement(models.Model):
    """Modèle représentant un mouvement de matériel."""
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('perception', 'Perception'),
        ('reversement', 'Reversement'),
    ]

    type = models.CharField('Type de mouvement', max_length=50, choices=TYPE_CHOICES, default='entree')
    date = models.DateField('Date du mouvement')
    materiel = models.ForeignKey(
        Materiel, on_delete=models.CASCADE,
        related_name='mouvements', verbose_name='Matériel'
    )
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE,
        related_name='mouvements', verbose_name='Document'
    )
    quantite = models.IntegerField('Quantité', default=1)
    observations = models.TextField('Observations', blank=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        db_table = 'core_mouvement'
        verbose_name = 'Mouvement'
        verbose_name_plural = 'Mouvements'
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_display()} - {self.materiel.designation} ({self.date.strftime('%d/%m/%Y')})"

    def get_absolute_url(self):
        return reverse('mouvement_list')


# ──────────────────────────────────────────────────────────────────────────────
# INVENTAIRE LOGISTIQUE (Tableau logistique militaire)
# ──────────────────────────────────────────────────────────────────────────────

class CategorieMaterielLogistique(models.Model):
    """Catégorie de matériel pour le tableau logistique."""
    CATEGORIE_CHOICES = [
        ('radar',      'MAT RADAR'),
        ('uhf',        'MAT RADIO UHF'),
        ('vhf_groupe', 'MAT RADIO VHF NIVEAU GROUPE'),
        ('vhf_cie',    'MAT RADIO VHF NIVEAU COMPAGNIE'),
        ('hf',         'MAT RADIO HF'),
    ]

    code  = models.CharField('Code', max_length=20, choices=CATEGORIE_CHOICES, unique=True)
    ordre = models.PositiveSmallIntegerField('Ordre d\'affichage', default=0)

    class Meta:
        db_table = 'core_categorie_logistique'
        verbose_name = 'Catégorie Logistique'
        verbose_name_plural = 'Catégories Logistiques'
        ordering = ['ordre']

    def __str__(self):
        return self.get_code_display()


class LigneInventaireLogistique(models.Model):
    """
    Ligne du tableau logistique militaire.

    Contrainte : QTE = SVC + MAG + REP
    Répartition SVC : GMI + GS + GCS
    """
    categorie   = models.ForeignKey(
        CategorieMaterielLogistique,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Catégorie'
    )
    designation = models.CharField('Désignation du matériel', max_length=300)
    ordre       = models.PositiveSmallIntegerField('Ordre dans la catégorie', default=0)

    # Position
    qte = models.PositiveIntegerField('Quantité totale', default=0)
    svc = models.PositiveIntegerField('SVC (En service)', default=0)
    mag = models.PositiveIntegerField('MAG (Magasin)', default=0)
    rep = models.PositiveIntegerField('REP (Réparation)', default=0)

    # Répartition matériels en service
    gmi = models.PositiveIntegerField('GMI', default=0)
    gs  = models.PositiveIntegerField('GS',  default=0)
    gcs = models.PositiveIntegerField('GCS', default=0)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_ligne_inventaire_logistique'
        verbose_name = 'Ligne Inventaire Logistique'
        verbose_name_plural = 'Lignes Inventaire Logistique'
        ordering = ['categorie__ordre', 'ordre', 'designation']

    def __str__(self):
        return f"{self.categorie} – {self.designation}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.qte != self.svc + self.mag + self.rep:
            raise ValidationError(
                f"QTE ({self.qte}) doit être égale à SVC + MAG + REP "
                f"({self.svc} + {self.mag} + {self.rep} = {self.svc + self.mag + self.rep})."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_repartition(self):
        return self.gmi + self.gs + self.gcs
