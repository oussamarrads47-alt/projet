# 🔐 Sécurité — TRANS-GEST

## Mesures de Sécurité Implémentées

### Authentification
- Système d'authentification Django intégré
- Décorateur `@login_required` sur toutes les vues
- Sessions sécurisées avec timeout
- URLs de connexion/déconnexion configurées

### Protection CSRF
- Middleware CSRF activé
- Tokens CSRF dans tous les formulaires
- Validation automatique par Django

### Protection contre les Injections SQL
- Utilisation exclusive de l'ORM Django
- Pas de requêtes SQL brutes dans le code applicatif
- Paramètres échappés automatiquement

### Gestion des Mots de Passe
Validateurs configurés dans `settings.py` :
- Similarité avec les attributs utilisateur
- Longueur minimale
- Mots de passe courants interdits
- Mots de passe entièrement numériques interdits

### Variables d'Environnement
- `SECRET_KEY` chargée depuis `.env`
- Mots de passe de base de données dans `.env`
- Fichier `.env` exclu du versioning Git

---

## Configuration de Production

### Paramètres à modifier

```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']

# Sécurité des cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Headers de sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Vérification
```bash
python manage.py check --deploy
```

---

## Rôles Utilisateurs

| Rôle | Accès Admin | Créer/Modifier | Visualiser |
|------|-------------|----------------|------------|
| Admin | ✅ | ✅ | ✅ |
| Manager | ✅ | ✅ | ✅ |
| Viewer | ❌ | ❌ | ✅ |

---

## Bonnes Pratiques

1. **Ne jamais** commiter le fichier `.env`
2. **Toujours** utiliser HTTPS en production
3. **Changer** la `SECRET_KEY` par défaut
4. **Maintenir** les dépendances à jour
5. **Sauvegarder** régulièrement la base de données
6. **Limiter** les `ALLOWED_HOSTS` aux domaines nécessaires
7. **Auditer** les logs régulièrement
