#!/bin/bash
# ============================================================
# TRANS-GEST : Script de configuration de la base de données
# Pour Linux / macOS
# ============================================================

set -e

echo "🎖️  TRANS-GEST - Configuration de la Base de Données"
echo "======================================================="

# Vérifier si PostgreSQL est installé
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL détecté"
    
    # Créer la base de données
    echo ""
    echo "📦 Création de la base de données..."
    sudo -u postgres psql -f database/create_database.sql
    
    echo ""
    echo "✅ Base de données PostgreSQL créée"
else
    echo "⚠️  PostgreSQL non détecté, utilisation de SQLite"
    echo "   Pour installer PostgreSQL :"
    echo "   - Ubuntu/Debian : sudo apt-get install postgresql postgresql-contrib"
    echo "   - macOS : brew install postgresql"
fi

# Activer l'environnement virtuel si disponible
if [ -d "venv" ]; then
    echo ""
    echo "🐍 Activation de l'environnement virtuel..."
    source venv/bin/activate
fi

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Exécuter les migrations
echo ""
echo "🗄️  Exécution des migrations..."
python manage.py makemigrations
python manage.py migrate

# Créer le superutilisateur
echo ""
echo "👤 Création du superutilisateur..."
echo "   (Suivez les instructions ci-dessous)"
python manage.py createsuperuser --username admin --email admin@transgest.ma

# Charger les données de test
echo ""
echo "📊 Chargement des données de test..."
python manage.py loaddata fixtures/magasins.json
python manage.py loaddata fixtures/detenteurs.json
python manage.py loaddata fixtures/materiels.json
python manage.py loaddata fixtures/documents.json
python manage.py loaddata fixtures/mouvements.json

# Collecter les fichiers statiques
echo ""
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer les répertoires media
echo ""
echo "📁 Création des répertoires media..."
mkdir -p media/materiels media/detenteurs

# Vérifier la connexion
echo ""
echo "🔍 Vérification de la connexion..."
python manage.py check_db

echo ""
echo "======================================================="
echo "✅ Configuration terminée avec succès !"
echo ""
echo "Pour démarrer le serveur :"
echo "  python manage.py runserver"
echo ""
echo "Accès :"
echo "  🌐 Application : http://localhost:8000/"
echo "  🔧 Admin       : http://localhost:8000/admin/"
echo "  📡 API         : http://localhost:8000/api/"
echo "======================================================="
