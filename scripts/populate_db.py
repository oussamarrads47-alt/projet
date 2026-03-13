#!/usr/bin/env python
"""
Script pour peupler la base de données avec des données réalistes.
Usage: python scripts/populate_db.py
"""
import os
import sys
import django

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Magasin, Detenteur, Materiel, Document, Mouvement
from datetime import date, timedelta
import random


def populate():
    """Peuple la base de données avec des données de démonstration."""

    print("🎖️  TRANS-GEST - Peuplement de la base de données")
    print("=" * 50)

    # Magasins
    magasins_data = [
        {'nom': 'Magasin Central Rabat', 'localisation': 'Quartier Général, Avenue des FAR, Rabat'},
        {'nom': 'Magasin Nord Tanger', 'localisation': 'Base Militaire Nord, Route de Tétouan, Tanger'},
        {'nom': 'Magasin Sud Agadir', 'localisation': 'Caserne Militaire Sud, Boulevard Hassan II, Agadir'},
    ]
    magasins = []
    for data in magasins_data:
        mag, created = Magasin.objects.get_or_create(**data)
        magasins.append(mag)
        status = "créé" if created else "existant"
        print(f"  📦 Magasin {status}: {mag.nom}")

    # Détenteurs
    detenteurs_data = [
        {'nom': 'Unité Transmissions Alpha', 'grade': 'colonel', 'fonction': 'Chef de Corps'},
        {'nom': 'Section Communication Bravo', 'grade': 'commandant', 'fonction': 'Chef de Section'},
        {'nom': 'Peloton Radio Charlie', 'grade': 'capitaine', 'fonction': 'Chef de Peloton'},
        {'nom': 'Équipe Technique Delta', 'grade': 'lieutenant', 'fonction': 'Chef d\'Équipe'},
    ]
    detenteurs = []
    for data in detenteurs_data:
        det, created = Detenteur.objects.get_or_create(**data)
        detenteurs.append(det)
        status = "créé" if created else "existant"
        print(f"  👤 Détenteur {status}: {det}")

    # Matériels
    materiels_data = [
        {'designation': 'Radio SINCGARS RT-1523', 'type_materiel': 'radio', 'numero_serie': 'SN-SINC-001', 'etat': 'service'},
        {'designation': 'Radio VHF AN/PRC-152', 'type_materiel': 'radio', 'numero_serie': 'SN-VHF-002', 'etat': 'service'},
        {'designation': 'Système de Communication Tactique', 'type_materiel': 'radio', 'numero_serie': 'SN-SCT-003', 'etat': 'service'},
        {'designation': 'Ordinateur Portable Durci Getac', 'type_materiel': 'informatique', 'numero_serie': 'SN-OPD-004', 'etat': 'service'},
        {'designation': 'Véhicule HMMWV Communication', 'type_materiel': 'vehicule', 'numero_serie': 'SN-VHC-005', 'etat': 'service'},
        {'designation': 'Antenne Satellite Militaire', 'type_materiel': 'radio', 'numero_serie': 'SN-ASM-006', 'etat': 'attente'},
        {'designation': 'Radio Tactique AN/PRC-117G', 'type_materiel': 'radio', 'numero_serie': 'SN-RT-007', 'etat': 'service'},
        {'designation': 'Jumelles Vision Nocturne AN/PVS-14', 'type_materiel': 'optique', 'numero_serie': 'SN-JVN-008', 'etat': 'service'},
        {'designation': 'GPS Militaire Defense Advanced', 'type_materiel': 'informatique', 'numero_serie': 'SN-GPS-009', 'etat': 'service'},
        {'designation': 'Générateur Tactique MEP-803A', 'type_materiel': 'autre', 'numero_serie': 'SN-GEN-010', 'etat': 'attente'},
        {'designation': 'Système Cryptographie KG-250', 'type_materiel': 'informatique', 'numero_serie': 'SN-CRY-011', 'etat': 'service'},
        {'designation': 'Caméra Thermique FLIR Black Hornet', 'type_materiel': 'optique', 'numero_serie': 'SN-CTH-012', 'etat': 'service'},
        {'designation': 'Tablette Militaire Samsung Galaxy Tab', 'type_materiel': 'informatique', 'numero_serie': 'SN-TAB-013', 'etat': 'hors_service'},
        {'designation': 'Radio Portative Harris RF-300', 'type_materiel': 'radio', 'numero_serie': 'SN-RPH-014', 'etat': 'service'},
        {'designation': 'Station Radio Mobile JCCS', 'type_materiel': 'radio', 'numero_serie': 'SN-SRM-015', 'etat': 'service'},
        {'designation': 'Système Téléconférence Sécurisé', 'type_materiel': 'telephonique', 'numero_serie': 'SN-STS-016', 'etat': 'service'},
        {'designation': 'Drone Reconnaissance RQ-11 Raven', 'type_materiel': 'autre', 'numero_serie': 'SN-DRN-017', 'etat': 'approvisionnement'},
        {'designation': 'Serveur Tactique HPE', 'type_materiel': 'informatique', 'numero_serie': 'SN-SRV-018', 'etat': 'service'},
        {'designation': 'Casque Communication Peltor COMTAC', 'type_materiel': 'radio', 'numero_serie': 'SN-CSQ-019', 'etat': 'service'},
        {'designation': 'Kit Météorologique Kestrel 5500', 'type_materiel': 'autre', 'numero_serie': 'SN-MET-020', 'etat': 'service'},
    ]
    materiels = []
    for i, data in enumerate(materiels_data):
        data['magasin'] = magasins[i % len(magasins)]
        data['detenteur'] = detenteurs[i % len(detenteurs)] if random.random() > 0.3 else None
        mat, created = Materiel.objects.get_or_create(
            numero_serie=data['numero_serie'], defaults=data
        )
        materiels.append(mat)
        status = "créé" if created else "existant"
        print(f"  🔧 Matériel {status}: {mat.designation}")

    # Documents
    for i in range(10):
        doc_date = date.today() - timedelta(days=random.randint(1, 365))
        doc_type = random.choice(['50/4', '50/5', '50/6', '50/7', '50/8'])
        Document.objects.get_or_create(
            type=doc_type,
            date=doc_date,
            defaults={'description': f'Document {doc_type} du {doc_date.strftime("%d/%m/%Y")}'}
        )

    print(f"\n📊 Résumé :")
    print(f"  Magasins    : {Magasin.objects.count()}")
    print(f"  Détenteurs  : {Detenteur.objects.count()}")
    print(f"  Matériels   : {Materiel.objects.count()}")
    print(f"  Documents   : {Document.objects.count()}")
    print(f"  Mouvements  : {Mouvement.objects.count()}")
    print(f"\n✅ Peuplement terminé !")


if __name__ == '__main__':
    populate()
