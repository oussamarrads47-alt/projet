#!/bin/bash
# ============================================================
# TRANS-GEST : Sauvegarde des fichiers media
# ============================================================

BACKUP_DIR="backups/media_$(date +%Y%m%d_%H%M%S)"

echo "🎖️  TRANS-GEST - Sauvegarde des fichiers media"
echo "================================================"

# Créer le répertoire de sauvegarde
mkdir -p "$BACKUP_DIR"

# Sauvegarder les fichiers media
if [ -d "media" ]; then
    echo "📦 Sauvegarde du répertoire media..."
    cp -r media/* "$BACKUP_DIR/" 2>/dev/null
    
    # Compresser la sauvegarde
    tar -czf "${BACKUP_DIR}.tar.gz" -C backups "$(basename $BACKUP_DIR)"
    rm -rf "$BACKUP_DIR"
    
    echo "✅ Sauvegarde créée : ${BACKUP_DIR}.tar.gz"
    echo "📊 Taille : $(du -sh "${BACKUP_DIR}.tar.gz" | cut -f1)"
else
    echo "⚠️  Aucun répertoire media trouvé"
fi

echo ""
echo "📋 Sauvegardes disponibles :"
ls -lh backups/media_*.tar.gz 2>/dev/null || echo "  Aucune sauvegarde"
