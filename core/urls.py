"""
URL patterns pour l'application core de TRANS-GEST.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),

    # Dashboard
    path('welcome/', views.welcome_view, name='welcome'),
    path('situation/', views.situation_view, name='situation_report'),
    path('', views.dashboard, name='dashboard'),

    # Search
    path('search/', views.search_view, name='search'),

    # Matériels
    path('materiels/', views.materiel_list, name='materiel_list'),
    path('materiels/create/', views.materiel_create, name='materiel_create'),
    path('materiels/<int:pk>/', views.materiel_detail, name='materiel_detail'),
    path('materiels/<int:pk>/edit/', views.materiel_update, name='materiel_update'),
    path('materiels/<int:pk>/delete/', views.materiel_delete, name='materiel_delete'),

    # Magasins
    path('magasins/', views.magasin_list, name='magasin_list'),
    path('magasins/create/', views.magasin_create, name='magasin_create'),
    path('magasins/<int:pk>/edit/', views.magasin_update, name='magasin_update'),
    path('magasins/<int:pk>/delete/', views.magasin_delete, name='magasin_delete'),

    # Détenteurs
    path('detenteurs/', views.detenteur_list, name='detenteur_list'),
    path('detenteurs/create/', views.detenteur_create, name='detenteur_create'),
    path('detenteurs/<int:pk>/edit/', views.detenteur_update, name='detenteur_update'),
    path('detenteurs/<int:pk>/delete/', views.detenteur_delete, name='detenteur_delete'),

    # Documents
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<int:pk>/edit/', views.document_update, name='document_update'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),

    # Mouvements
    path('mouvements/', views.mouvement_list, name='mouvement_list'),
    path('mouvements/create/', views.mouvement_create, name='mouvement_create'),
    path('mouvements/<int:pk>/edit/', views.mouvement_update, name='mouvement_update'),
    path('mouvements/<int:pk>/delete/', views.mouvement_delete, name='mouvement_delete'),

    # Exports
    path('export/materiels/excel/', views.export_materiels_excel, name='export_materiels_excel'),
    path('export/materiels/csv/', views.export_materiels_csv, name='export_materiels_csv'),
    path('export/materiels/pdf/', views.export_materiels_pdf, name='export_materiels_pdf'),

    # Inventaire Logistique
    path('inventaire/', views.inventaire_logistique, name='inventaire_logistique'),
]
