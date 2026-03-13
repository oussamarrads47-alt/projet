# 🎖️ TRANS-GEST

## Système de Gestion des Matériels de Transmission

---

## 🇫🇷 Description

**TRANS-GEST** est une application web professionnelle développée avec Django pour la gestion des équipements de communication militaire. Elle permet le suivi complet des matériels de transmission, des magasins, des détenteurs, des documents et des mouvements.

## 🇬🇧 Description (English)

**TRANS-GEST** is a professional web application built with Django for managing military transmission equipment. It provides complete tracking of communication equipment, warehouses, holders, documents, and movements.

---

## ✨ Fonctionnalités

- 📦 **Gestion des Matériels** — CRUD complet pour les équipements militaires
- 🏪 **Gestion des Magasins** — Suivi des entrepôts et emplacements
- 👤 **Gestion des Détenteurs** — Gestion des unités et responsables
- 📄 **Gestion des Documents** — Types 50/4 à 50/8 et autres
- 🔄 **Suivi des Mouvements** — Entrées, sorties, perceptions, reversements
- 📊 **Tableau de Bord** — Statistiques et visualisations en temps réel
- 📡 **API REST** — Endpoints RESTful pour toutes les entités
- 🔍 **Recherche Avancée** — Recherche et filtrage multi-critères
- 📥 **Export** — PDF, Excel, CSV
- 🎨 **Design Moderne** — Interface glassmorphism avec animation Three.js
- 🔐 **Authentification** — Système de connexion sécurisé
- 📱 **Responsive** — Compatible mobile, tablette, desktop

---

## 🛠️ Technologies

| Composant | Technologie |
|-----------|-------------|
| Backend | Django 5.0+ |
| API | Django REST Framework |
| Base de données | PostgreSQL / SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Animation | Three.js |
| Formulaires | django-crispy-forms |
| Export PDF | ReportLab |
| Export Excel | openpyxl |
| Serveur WSGI | Gunicorn |
| Conteneur | Docker |

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.11+
- pip
- PostgreSQL (optionnel, SQLite par défaut)

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd monprojet
```

### 2. Environnement virtuel
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

### 5. Base de données
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Données de test
```bash
python manage.py loaddata fixtures/magasins.json
python manage.py loaddata fixtures/detenteurs.json
python manage.py loaddata fixtures/materiels.json
python manage.py loaddata fixtures/documents.json
python manage.py loaddata fixtures/mouvements.json
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

### 8. Accéder à l'application
- 🌐 **Application** : http://localhost:8000/
- 🔧 **Admin** : http://localhost:8000/admin/
- 📡 **API** : http://localhost:8000/api/

### 🔑 Comptes de Test (Par défaut)

| Rôle | Username | Email | Mot de Passe |
|------|----------|-------|--------------|
| **Administrateur** | `admin` | `admin@transgest.ma` | `admin123` |
| **Gestionnaire** | `manager` | `manager@transgest.ma` | `manager123` |
| **Visualiseur** | `viewer` | `viewer@transgest.ma` | `viewer123` |

---

## 📁 Structure du Projet

```
monprojet/
├── manage.py
├── requirements.txt
├── config/                 # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                   # Application principale
│   ├── models.py           # 5 modèles (Magasin, Detenteur, Materiel, Document, Mouvement)
│   ├── views.py            # Vues CRUD + Dashboard
│   ├── urls.py             # Routes de l'application
│   ├── forms.py            # Formulaires Django
│   ├── admin.py            # Configuration admin
│   ├── serializers.py      # Serializers DRF
│   ├── api_views.py        # ViewSets API
│   ├── templates/          # Templates HTML
│   ├── static/             # CSS, JS, images
│   ├── tests/              # Tests unitaires
│   └── management/commands/ # Commandes personnalisées
├── fixtures/               # Données de test
├── database/               # Scripts de base de données
├── scripts/                # Scripts utilitaires
├── media/                  # Fichiers uploadés
├── logs/                   # Fichiers de log
└── backups/                # Sauvegardes
```

---

## 🧪 Tests

```bash
# Tous les tests
python manage.py test core

# Tests spécifiques
python manage.py test core.tests.test_models
python manage.py test core.tests.test_views
python manage.py test core.tests.test_forms
python manage.py test core.tests.test_api
```

---

## 🐳 Docker

```bash
# Démarrer avec Docker Compose
docker-compose up --build

# Migrations
docker-compose exec web python manage.py migrate

# Superutilisateur
docker-compose exec web python manage.py createsuperuser
```

---

## 📡 API REST

| Endpoint | Méthodes | Description |
|----------|----------|-------------|
| `/api/magasins/` | GET, POST, PUT, DELETE | Gestion des magasins |
| `/api/detenteurs/` | GET, POST, PUT, DELETE | Gestion des détenteurs |
| `/api/materiels/` | GET, POST, PUT, DELETE | Gestion des matériels |
| `/api/documents/` | GET, POST, PUT, DELETE | Gestion des documents |
| `/api/mouvements/` | GET, POST, PUT, DELETE | Gestion des mouvements |

---

## 📧 Contact

- **Projet** : TRANS-GEST v2.0
- **Localisation** : Rabat, Maroc
- **Téléphone** : +212 522 123 456
- **Email** : contact@transgest.ma

---

## 📄 Licence

Ce projet est propriétaire. Tous droits réservés © 2024.
