# 🗄️ Schéma de Base de Données — TRANS-GEST

## Diagramme Entité-Relation

```
┌──────────────────┐         ┌────────────────────────┐         ┌──────────────────┐
│     Magasin      │────────>│      Materiel          │<────────│    Detenteur      │
│                  │   1:N   │                        │   N:1   │                  │
│ - id (PK)        │         │ - id (PK)              │         │ - id (PK)        │
│ - nom            │         │ - designation          │         │ - nom            │
│ - localisation   │         │ - type_materiel        │         │ - grade          │
│ - created_at     │         │ - numero_serie (UNIQUE)│         │ - fonction       │
│ - updated_at     │         │ - etat                 │         │ - image          │
└──────────────────┘         │ - magasin_id (FK)      │         │ - created_at     │
                             │ - detenteur_id (FK)    │         │ - updated_at     │
                             │ - image                │         └──────────────────┘
                             │ - date_sortie          │
                             │ - date_retour          │
                             │ - created_at           │
                             │ - updated_at           │
                             └────────────────────────┘
                                        │
                                        │ 1:N
                                        ▼
                             ┌────────────────────────┐
                             │      Mouvement         │
                             │                        │
                             │ - id (PK)              │
                             │ - type                 │
                             │ - date                 │
                             │ - materiel_id (FK) ────│──> Materiel
                             │ - document_id (FK) ────│──> Document
                             │ - quantite             │
                             │ - observations         │
                             │ - created_at           │
                             │ - updated_at           │
                             └────────────────────────┘
                                        │
                                        │ N:1
                                        ▼
                             ┌────────────────────────┐
                             │      Document          │
                             │                        │
                             │ - id (PK)              │
                             │ - type                 │
                             │ - date                 │
                             │ - description          │
                             │ - date_sortie          │
                             │ - date_retour          │
                             │ - observations         │
                             │ - created_at           │
                             │ - updated_at           │
                             └────────────────────────┘
```

---

## Tables

### core_magasin
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | BigAutoField | PRIMARY KEY |
| nom | VARCHAR(200) | NOT NULL |
| localisation | VARCHAR(300) | NOT NULL |
| created_at | DATETIME | auto_now_add |
| updated_at | DATETIME | auto_now |

### core_detenteur
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | BigAutoField | PRIMARY KEY |
| nom | VARCHAR(200) | NOT NULL |
| grade | VARCHAR(100) | NOT NULL, CHOICES |
| fonction | VARCHAR(200) | NOT NULL |
| image | VARCHAR(100) | NULLABLE |
| created_at | DATETIME | auto_now_add |
| updated_at | DATETIME | auto_now |

**Grades :** soldat, caporal, sergent, adjudant, lieutenant, capitaine, commandant, colonel, général

### core_materiel
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | BigAutoField | PRIMARY KEY |
| designation | VARCHAR(300) | NOT NULL |
| type_materiel | VARCHAR(100) | NOT NULL, CHOICES |
| numero_serie | VARCHAR(100) | UNIQUE, NOT NULL |
| etat | VARCHAR(50) | NOT NULL, CHOICES |
| magasin_id | BigInt | FK → core_magasin, CASCADE |
| detenteur_id | BigInt | FK → core_detenteur, SET_NULL, NULLABLE |
| image | VARCHAR(100) | NULLABLE |
| date_sortie | DATE | NULLABLE |
| date_retour | DATE | NULLABLE |
| created_at | DATETIME | auto_now_add |
| updated_at | DATETIME | auto_now |

**Types :** radio, telephonique, informatique, vehicule, armement, optique, autre
**États :** service, attente, approvisionnement, hors_service

**Index :** numero_serie, etat, type_materiel, (magasin, etat), -created_at

### core_document
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | BigAutoField | PRIMARY KEY |
| type | VARCHAR(50) | NOT NULL, CHOICES |
| date | DATE | NOT NULL |
| description | TEXT | BLANK |
| date_sortie | DATE | NULLABLE |
| date_retour | DATE | NULLABLE |
| observations | TEXT | BLANK |
| created_at | DATETIME | auto_now_add |
| updated_at | DATETIME | auto_now |

**Types :** 50/4, 50/5, 50/6, 50/7, 50/8, autre

### core_mouvement
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | BigAutoField | PRIMARY KEY |
| type | VARCHAR(50) | NOT NULL, CHOICES |
| date | DATE | NOT NULL |
| materiel_id | BigInt | FK → core_materiel, CASCADE |
| document_id | BigInt | FK → core_document, CASCADE |
| quantite | INTEGER | DEFAULT 1 |
| observations | TEXT | BLANK |
| created_at | DATETIME | auto_now_add |
| updated_at | DATETIME | auto_now |

**Types :** entree, sortie, perception, reversement
