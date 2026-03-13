# 📋 Changelog — TRANS-GEST

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

---

## [2.0.0] — 2024-01-01

### Ajouté
- Application Django complète avec 5 modèles (Magasin, Detenteur, Materiel, Document, Mouvement)
- Interface web avec animation Three.js (particules interactives)
- Design glassmorphism avec thème bleu/blanc
- Tableau de bord avec 8 cartes de statistiques
- CRUD complet pour toutes les entités
- API REST avec Django REST Framework
- Système d'authentification avec rôles (Admin, Manager, Viewer)
- Export PDF (ReportLab) et Excel (openpyxl)
- Recherche avancée multi-modèles
- Pagination (20 éléments par page)
- Panel d'administration Django personnalisé
- Fixtures avec 20 matériels militaires réalistes
- Commandes de gestion : `check_db`, `backup_db`, `db_stats`, `db_health`, `load_sample_data`
- Configuration Docker (Dockerfile, docker-compose.yml, nginx.conf)
- Scripts de déploiement (Heroku, VPS)
- Documentation complète (README, INSTALLATION, DEPLOYMENT, API, SECURITY)
- Tests unitaires (modèles, vues, formulaires, API)
- Support PostgreSQL et SQLite
- Interface entièrement en français
- Design responsive (5→4→3→2→1 colonnes)
- Fuseau horaire Maroc (Africa/Casablanca)

### Configuration
- Django 5.0+
- Python 3.11+
- Base de données : PostgreSQL (prod) / SQLite (dev)
- Serveur : Gunicorn + Nginx (prod)

---

## [1.0.0] — 2024-01-01

### Ajouté
- Version initiale du projet
- Structure Django de base
- Modèles de données
- Vues CRUD basiques
