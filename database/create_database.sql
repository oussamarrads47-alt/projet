
-- Créer la base de données
CREATE DATABASE transgest_db
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'fr_FR.UTF-8'
    LC_CTYPE = 'fr_FR.UTF-8'
    TEMPLATE = template0;

-- Créer l'utilisateur
CREATE USER transgest_user WITH PASSWORD 'your_secure_password_here';

-- Accorder les privilèges
GRANT ALL PRIVILEGES ON DATABASE transgest_db TO transgest_user;

-- Se connecter à la base de données
\c transgest_db

-- Accorder les privilèges sur le schéma
GRANT ALL ON SCHEMA public TO transgest_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO transgest_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO transgest_user;

-- Configurer les paramètres par défaut pour l'utilisateur
ALTER ROLE transgest_user SET client_encoding TO 'utf8';
ALTER ROLE transgest_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE transgest_user SET timezone TO 'Africa/Casablanca';

-- Message de confirmation
\echo '✅ Base de données transgest_db créée avec succès !'
\echo '👤 Utilisateur transgest_user créé.'
\echo '🔑 N oubliez pas de changer le mot de passe !'
