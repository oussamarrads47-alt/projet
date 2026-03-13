# 🚀 Guide de Déploiement — TRANS-GEST

## Option 1 : Docker (Recommandé)

### Démarrage rapide
```bash
docker-compose up --build -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py loaddata fixtures/magasins.json
```

### Commandes utiles
```bash
docker-compose logs -f web     # Voir les logs
docker-compose down            # Arrêter
docker-compose down -v         # Arrêter + supprimer volumes
```

---

## Option 2 : Heroku

### Prérequis
- Heroku CLI installé
- Compte Heroku

### Déploiement
```bash
heroku create transgest-app
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Variables d'environnement
```bash
heroku config:set SECRET_KEY='votre-clé-secrète'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=transgest-app.herokuapp.com
heroku config:set DB_ENGINE=postgresql
```

---

## Option 3 : VPS (DigitalOcean / AWS / OVH)

### 1. Préparer le serveur
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv postgresql nginx -y
```

### 2. Installer l'application
```bash
cd /home
git clone <repo-url> transgest
cd transgest
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3. Configurer PostgreSQL
```bash
sudo -u postgres psql -f database/create_database.sql
```

### 4. Configurer l'environnement
```bash
cp .env.example .env
nano .env  # Configurer pour la production
```

Important en production :
```
DEBUG=False
SECRET_KEY=clé-très-longue-et-aléatoire
ALLOWED_HOSTS=votre-domaine.com
```

### 5. Appliquer les migrations
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Configurer Gunicorn (service systemd)

Créer `/etc/systemd/system/transgest.service` :
```ini
[Unit]
Description=TRANS-GEST Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/transgest
Environment="PATH=/home/transgest/venv/bin"
ExecStart=/home/transgest/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/transgest/transgest.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start transgest
sudo systemctl enable transgest
```

### 7. Configurer Nginx

Le fichier `nginx.conf` fourni peut être copié dans `/etc/nginx/nginx.conf`, en ajustant `server_name` avec votre domaine.

```bash
sudo systemctl restart nginx
```

---

## Checklist de Production

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` unique et fort
- [ ] `ALLOWED_HOSTS` configuré
- [ ] PostgreSQL (pas SQLite)
- [ ] HTTPS activé (Let's Encrypt / Certbot)
- [ ] Fichiers statiques collectés
- [ ] Logs configurés
- [ ] Backups automatisés
- [ ] `python manage.py check --deploy` sans erreurs
