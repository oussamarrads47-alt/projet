"""
Configuration de l'administration Django pour TRANS-GEST.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Magasin, Detenteur, Materiel, Document, Mouvement, \
    CategorieMaterielLogistique, LigneInventaireLogistique


# --- Admin Site Configuration ---
admin.site.site_header = '🎖️ TRANS-GEST Administration'
admin.site.site_title = 'TRANS-GEST Admin'
admin.site.index_title = 'Gestion des Matériels de Transmission'


@admin.register(Magasin)
class MagasinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'localisation', 'nombre_materiels', 'created_at')
    search_fields = ('nom', 'localisation')
    list_filter = ('created_at',)

    def nombre_materiels(self, obj):
        return obj.materiels.count()
    nombre_materiels.short_description = 'Nb Matériels'


@admin.register(Detenteur)
class DetenteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'grade', 'fonction', 'image_preview', 'nombre_materiels', 'created_at')
    search_fields = ('nom', 'fonction')
    list_filter = ('grade', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;object-fit:cover;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Photo'

    def nombre_materiels(self, obj):
        return obj.materiels.count()
    nombre_materiels.short_description = 'Nb Matériels'


@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('designation', 'type_materiel', 'numero_serie', 'etat_badge', 'magasin', 'detenteur', 'image_preview', 'created_at')
    search_fields = ('designation', 'numero_serie')
    list_filter = ('etat', 'type_materiel', 'magasin', 'detenteur')
    raw_id_fields = ('magasin', 'detenteur')

    def etat_badge(self, obj):
        colors = {
            'service': '#4ade80',
            'attente': '#fb923c',
            'approvisionnement': '#3b82f6',
            'hors_service': '#ef4444',
        }
        color = colors.get(obj.etat, '#94a3b8')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; border-radius:12px; font-size:12px;">{}</span>',
            color, obj.get_etat_display()
        )
    etat_badge.short_description = 'État'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="40" style="border-radius:8px;object-fit:cover;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Photo'

    actions = ['marquer_en_service', 'marquer_hors_service']

    @admin.action(description='Marquer en service')
    def marquer_en_service(self, request, queryset):
        queryset.update(etat='service')

    @admin.action(description='Marquer hors service')
    def marquer_hors_service(self, request, queryset):
        queryset.update(etat='hors_service')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'description_courte', 'date_sortie', 'date_retour', 'nombre_mouvements')
    search_fields = ('description', 'observations')
    list_filter = ('type', 'date')

    def description_courte(self, obj):
        return obj.description[:80] + '…' if len(obj.description) > 80 else obj.description
    description_courte.short_description = 'Description'

    def nombre_mouvements(self, obj):
        return obj.mouvements.count()
    nombre_mouvements.short_description = 'Nb Mouvements'


@admin.register(Mouvement)
class MouvementAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'materiel', 'document', 'quantite', 'observations_courtes')
    search_fields = ('materiel__designation', 'observations')
    list_filter = ('type', 'date')
    raw_id_fields = ('materiel', 'document')

    def observations_courtes(self, obj):
        return obj.observations[:60] + '…' if len(obj.observations) > 60 else obj.observations
    observations_courtes.short_description = 'Observations'


# ── Inventaire Logistique ──────────────────────────────────────────────────────

class LigneInventaireLogistiqueInline(admin.TabularInline):
    model = LigneInventaireLogistique
    extra = 1
    fields = ('designation', 'ordre', 'qte', 'svc', 'mag', 'rep', 'gmi', 'gs', 'gcs')
    ordering = ('ordre', 'designation')


@admin.register(CategorieMaterielLogistique)
class CategorieMaterielLogistiqueAdmin(admin.ModelAdmin):
    list_display  = ('get_code_display', 'ordre', 'nb_lignes')
    ordering      = ('ordre',)
    inlines       = [LigneInventaireLogistiqueInline]

    def nb_lignes(self, obj):
        return obj.lignes.count()
    nb_lignes.short_description = 'Nb lignes'


@admin.register(LigneInventaireLogistique)
class LigneInventaireLogistiqueAdmin(admin.ModelAdmin):
    list_display  = ('designation', 'categorie', 'qte', 'svc', 'mag', 'rep', 'gmi', 'gs', 'gcs')
    list_filter   = ('categorie',)
    search_fields = ('designation',)
    ordering      = ('categorie__ordre', 'ordre', 'designation')
    fieldsets = (
        ('Identification', {
            'fields': ('categorie', 'designation', 'ordre')
        }),
        ('Position', {
            'fields': ('qte', 'svc', 'mag', 'rep'),
            'description': 'Contrainte : QTE = SVC + MAG + REP'
        }),
        ('Répartition Mat en SVC', {
            'fields': ('gmi', 'gs', 'gcs')
        }),
    )
