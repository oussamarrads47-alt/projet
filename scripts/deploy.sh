#!/bin/bash
# ============================================================
# TRANS-GEST : Script de déploiement automatisé
# ============================================================

set -e

echo "🎖️  TRANS-GEST - Déploiement"
echo "=============================="

# Variables
APP_DIR=$(pwd)
VENV_DIR="$APP_DIR/venv"

# Activer l'environnement virtuel
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
fi

# Mettre à jour les dépendances
echo "📦 Mise à jour des dépendances..."
pip install -r requirements.txt

# Exécuter les migrations
echo "🗄️  Exécution des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Vérification
echo "🔍 Vérification du déploiement..."
python manage.py check --deploy 2>&1 || true

# Statistiques
echo ""
echo "📊 Statistiques de la base :"
python manage.py db_stats

echo ""
echo "✅ Déploiement terminé !"
echo "   Redémarrez le serveur (gunicorn/uwsgi) pour appliquer les changements."
