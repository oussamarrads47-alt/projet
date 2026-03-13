#!/bin/bash
# ============================================================
# TRANS-GEST : Exécution de tous les tests
# ============================================================

echo "🎖️  TRANS-GEST - Exécution des Tests"
echo "======================================="

# Activer l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Tests des modèles
echo ""
echo "📋 Tests des modèles..."
python manage.py test core.tests.test_models -v 2

# Tests des vues
echo ""
echo "🌐 Tests des vues..."
python manage.py test core.tests.test_views -v 2

# Tests des formulaires
echo ""
echo "📝 Tests des formulaires..."
python manage.py test core.tests.test_forms -v 2

# Tests de l'API
echo ""
echo "📡 Tests de l'API..."
python manage.py test core.tests.test_api -v 2

# Tous les tests
echo ""
echo "🔄 Exécution complète..."
python manage.py test core -v 2

echo ""
echo "✅ Tous les tests terminés !"
