# 🔄 Guide de Migration — TRANS-GEST

## Commandes de Base

### Créer les migrations
```bash
python manage.py makemigrations core
```

### Visualiser les migrations
```bash
python manage.py showmigrations
```

### Appliquer les migrations
```bash
python manage.py migrate
```

### Vérifier l'état
```bash
python manage.py migrate --check
```

---

## Bonnes Pratiques

### 1. Toujours sauvegarder avant une migration
```bash
python manage.py backup_db
```

### 2. Tester sur le développement d'abord
```bash
# Environnement dev
python manage.py migrate

# Vérifier
python manage.py check_db
python manage.py db_stats
```

### 3. Migrations en production
```bash
# 1. Sauvegarder
python manage.py backup_db

# 2. Appliquer
python manage.py migrate --noinput

# 3. Vérifier
python manage.py db_health
```

---

## Scénarios Courants

### Ajouter un champ
```python
# models.py
class Materiel(models.Model):
    nouveau_champ = models.CharField(max_length=100, default='', blank=True)
```
```bash
python manage.py makemigrations core --name ajouter_nouveau_champ
python manage.py migrate
```

### Modifier un champ
```bash
python manage.py makemigrations core --name modifier_champ
python manage.py migrate
```

### Migration de données
```bash
python manage.py makemigrations --empty core --name migration_donnees
```

Éditer le fichier créé pour ajouter vos opérations de données.

### Annuler une migration
```bash
# Revenir à une migration précédente
python manage.py migrate core 0001_initial
```

### Réinitialiser les migrations (développement uniquement)
```bash
# ⚠️ ATTENTION : Supprime toutes les données
python manage.py flush
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

---

## Résolution de Problèmes

| Problème | Solution |
|----------|----------|
| Conflit de migration | `python manage.py makemigrations --merge` |
| Migration corrompue | Supprimer le fichier, recréer avec `makemigrations` |
| Table déjà existante | `python manage.py migrate --fake` |
| Données incohérentes | Restaurer depuis la sauvegarde |
