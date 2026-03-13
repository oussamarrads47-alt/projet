# 📦 Guide d'Installation — TRANS-GEST

## Prérequis

| Logiciel | Version Minimum | Obligatoire |
|----------|----------------|-------------|
| Python | 3.11+ | ✅ |
| pip | 23.0+ | ✅ |
| PostgreSQL | 15+ | ❌ (SQLite par défaut) |
| Git | 2.0+ | ❌ |
| Docker | 24.0+ | ❌ |

---

## Installation Détaillée

### 1. Cloner le dépôt
```bash
git clone <url-du-repo>
cd monprojet
```

### 2. Créer l'environnement virtuel

**Linux / macOS :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell) :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer l'environnement

Copier le fichier d'exemple :
```bash
cp .env.example .env
```

Éditer `.env` avec vos paramètres :
```
SECRET_KEY=votre-clé-secrète-unique
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=sqlite3
```

### 5. Option A — Base de données SQLite (Développement)

Aucune configuration supplémentaire requise. Définir `DB_ENGINE=sqlite3` dans `.env`.

```bash
python manage.py migrate
```

### 5. Option B — Base de données PostgreSQL (Production)

1. Installer PostgreSQL
2. Créer la base : `psql -U postgres -f database/create_database.sql`
3. Mettre à jour `.env` :
   ```
   DB_ENGINE=postgresql
   DB_NAME=transgest_db
   DB_USER=transgest_user
   DB_PASSWORD=votre_mot_de_passe
   DB_HOST=localhost
   DB_PORT=5432
   ```
4. Appliquer les migrations : `python manage.py migrate`

### 6. Créer le superutilisateur
```bash
python manage.py createsuperuser
```

### 7. Charger les données de démonstration
```bash
python manage.py loaddata fixtures/magasins.json
python manage.py loaddata fixtures/detenteurs.json
python manage.py loaddata fixtures/materiels.json
python manage.py loaddata fixtures/documents.json
python manage.py loaddata fixtures/mouvements.json
```

Ou en une seule commande :
```bash
python manage.py load_sample_data
```

### 8. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 9. Vérifier l'installation
```bash
python manage.py check_db
python manage.py db_stats
```

### 10. Lancer le serveur
```bash
python manage.py runserver
```

---

## Installation Automatisée

### Linux / macOS
```bash
chmod +x database/setup_database.sh
./database/setup_database.sh
```

### Windows
```powershell
.\database\setup_database.ps1
```

---

## Dépannage

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Vérifier que le venv est activé |
| Erreur de connexion PostgreSQL | Vérifier les paramètres dans `.env` |
| `Permission denied` | Exécuter en tant qu'administrateur |
| Erreur de migration | `python manage.py migrate --run-syncdb` |
| Fichiers statiques manquants | `python manage.py collectstatic` |
