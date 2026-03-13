# 🤝 Guide de Contribution — TRANS-GEST

## Comment Contribuer

### 1. Fork et Clone
```bash
git clone <votre-fork>
cd monprojet
```

### 2. Créer une branche
```bash
git checkout -b feature/ma-fonctionnalite
```

### 3. Développer
- Suivre les conventions PEP 8
- Ajouter des tests pour les nouvelles fonctionnalités
- Documenter avec des docstrings
- Utiliser des messages de commit clairs

### 4. Tester
```bash
python manage.py test core
```

### 5. Soumettre
```bash
git add .
git commit -m "feat: description de la fonctionnalité"
git push origin feature/ma-fonctionnalite
```
Créer une Pull Request sur le dépôt principal.

---

## Conventions

### Messages de Commit
- `feat:` — Nouvelle fonctionnalité
- `fix:` — Correction de bug
- `docs:` — Documentation
- `style:` — Formatage, pas de changement de logique
- `refactor:` — Refactoring du code
- `test:` — Ajout ou modification de tests
- `chore:` — Maintenance

### Code Python
- PEP 8
- Docstrings pour classes et fonctions
- Type hints quand approprié
- Texte de l'interface en français

### Templates HTML
- Indentation de 2 espaces
- Classes CSS descriptives
- Accessibilité (attributs alt, aria)

---

## Structure des Tests

```
core/tests/
├── test_models.py    # Tests des modèles
├── test_views.py     # Tests des vues
├── test_forms.py     # Tests des formulaires
└── test_api.py       # Tests de l'API
```

Chaque nouveau modèle ou vue doit avoir des tests correspondants.
