# ============================================================
# TRANS-GEST : Script de configuration de la base de données
# Pour Windows (PowerShell)
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================================"
Write-Host "  TRANS-GEST - Configuration de la Base de Donnees"
Write-Host "========================================================"
Write-Host ""

# Verifier si PostgreSQL est installe
$psqlPath = Get-Command psql -ErrorAction SilentlyContinue
if ($psqlPath) {
    Write-Host "PostgreSQL detecte"
    Write-Host "Creation de la base de donnees..."
    try {
        psql -U postgres -f database/create_database.sql
        Write-Host "Base de donnees PostgreSQL creee"
    } catch {
        Write-Host "Erreur lors de la creation de la base de donnees PostgreSQL"
        Write-Host "Usage de SQLite par defaut."
    }
} else {
    Write-Host "PostgreSQL non detecte, utilisation de SQLite"
}

# Python execution helper
$python = "python"
if (Test-Path "venv\Scripts\python.exe") {
    $python = ".\venv\Scripts\python.exe"
    Write-Host "Utilisation de l'environnement virtuel"
}

# Executer les migrations
Write-Host ""
Write-Host "Execution des migrations..."
& $python manage.py makemigrations
& $python manage.py migrate

# Charger les donnees de test
Write-Host ""
Write-Host "Chargement des donnees de test..."
& $python manage.py loaddata fixtures/users.json
& $python manage.py loaddata fixtures/magasins.json
& $python manage.py loaddata fixtures/detenteurs.json
& $python manage.py loaddata fixtures/materiels.json
& $python manage.py loaddata fixtures/documents.json
& $python manage.py loaddata fixtures/mouvements.json

# Collecter les fichiers statiques
Write-Host ""
Write-Host "Collecte des fichiers statiques..."
& $python manage.py collectstatic --noinput

# Creer les repertoires media
Write-Host ""
Write-Host "Creation des repertoires media..."
if (!(Test-Path "media\materiels")) { New-Item -ItemType Directory -Force -Path "media\materiels" | Out-Null }
if (!(Test-Path "media\detenteurs")) { New-Item -ItemType Directory -Force -Path "media\detenteurs" | Out-Null }

Write-Host ""
Write-Host "========================================================"
Write-Host "  Configuration terminee avec succes !"
Write-Host ""
Write-Host "  Pour demarrer le serveur :"
Write-Host "    python manage.py runserver"
Write-Host ""
Write-Host "  Acces :"
Write-Host "    Application : http://localhost:8000/"
Write-Host "========================================================"
