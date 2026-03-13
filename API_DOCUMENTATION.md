# 📡 Documentation API — TRANS-GEST

## Base URL
```
http://localhost:8000/api/
```

## Authentification
Toutes les requêtes API nécessitent une authentification par session Django.

---

## Magasins

### Lister les magasins
```
GET /api/magasins/
```
**Paramètres :** `?search=texte`, `?ordering=nom`

### Créer un magasin
```
POST /api/magasins/
Content-Type: application/json

{
    "nom": "Magasin Central",
    "localisation": "Rabat, Avenue des FAR"
}
```

### Détails d'un magasin
```
GET /api/magasins/{id}/
```

### Modifier un magasin
```
PUT /api/magasins/{id}/
Content-Type: application/json

{
    "nom": "Magasin Central Modifié",
    "localisation": "Rabat"
}
```

### Supprimer un magasin
```
DELETE /api/magasins/{id}/
```

---

## Détenteurs

### Lister les détenteurs
```
GET /api/detenteurs/
```
**Paramètres :** `?search=texte`, `?ordering=nom,grade`

### Créer un détenteur
```
POST /api/detenteurs/
Content-Type: application/json

{
    "nom": "Unité Alpha",
    "grade": "capitaine",
    "fonction": "Chef de section"
}
```
**Grades valides :** `soldat`, `caporal`, `sergent`, `adjudant`, `lieutenant`, `capitaine`, `commandant`, `colonel`, `general`

### Détails / Modifier / Supprimer
```
GET    /api/detenteurs/{id}/
PUT    /api/detenteurs/{id}/
DELETE /api/detenteurs/{id}/
```

---

## Matériels

### Lister les matériels
```
GET /api/materiels/
```
**Paramètres :** `?search=texte`, `?ordering=designation,etat`

### Créer un matériel
```
POST /api/materiels/
Content-Type: application/json

{
    "designation": "Radio AN/PRC-152",
    "type_materiel": "radio",
    "numero_serie": "SN-001",
    "etat": "service",
    "magasin": 1,
    "detenteur": 1
}
```
**Types :** `radio`, `telephonique`, `informatique`, `vehicule`, `armement`, `optique`, `autre`
**États :** `service`, `attente`, `approvisionnement`, `hors_service`

### Détails / Modifier / Supprimer
```
GET    /api/materiels/{id}/
PUT    /api/materiels/{id}/
DELETE /api/materiels/{id}/
```

---

## Documents

### Lister les documents
```
GET /api/documents/
```

### Créer un document
```
POST /api/documents/
Content-Type: application/json

{
    "type": "50/4",
    "date": "2024-01-15",
    "description": "Document de perception"
}
```
**Types :** `50/4`, `50/5`, `50/6`, `50/7`, `50/8`, `autre`

### Détails / Modifier / Supprimer
```
GET    /api/documents/{id}/
PUT    /api/documents/{id}/
DELETE /api/documents/{id}/
```

---

## Mouvements

### Lister les mouvements
```
GET /api/mouvements/
```

### Créer un mouvement
```
POST /api/mouvements/
Content-Type: application/json

{
    "type": "entree",
    "date": "2024-01-15",
    "materiel": 1,
    "document": 1,
    "quantite": 1,
    "observations": "Réception initiale"
}
```
**Types :** `entree`, `sortie`, `perception`, `reversement`

### Détails / Modifier / Supprimer
```
GET    /api/mouvements/{id}/
PUT    /api/mouvements/{id}/
DELETE /api/mouvements/{id}/
```

---

## Réponses

### Succès
- `200 OK` — Requête réussie
- `201 Created` — Ressource créée
- `204 No Content` — Suppression réussie

### Erreurs
- `400 Bad Request` — Données invalides
- `403 Forbidden` — Non authentifié
- `404 Not Found` — Ressource introuvable

### Pagination
```json
{
    "count": 20,
    "next": "http://localhost:8000/api/materiels/?page=2",
    "previous": null,
    "results": [...]
}
```
Taille de page par défaut : **20 éléments**.
