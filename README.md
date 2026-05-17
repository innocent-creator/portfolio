# Portfolio Freelance — Innocent ATCHA

Portfolio one-page professionnel développé avec Django 5.x, design glassmorphism sombre avec accents violet/bleu.

## Stack

- **Backend** : Django 5.x + Django REST Framework
- **Frontend** : HTML5, CSS3 vanilla, JavaScript ES6+
- **Styling** : CSS custom avec variables (design system complet)
- **Animations** : AOS (Animate On Scroll) + CSS transitions
- **Effets** : Particules canvas interactives sur le hero
- **BDD** : SQLite (dev) / PostgreSQL (prod)

## Installation rapide

```bash
# 1. Cloner le projet
git clone <repo-url>
cd portfolio

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configuration
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Base de données
python3 manage.py migrate

# 6. Charger les données de test
python3 manage.py loaddata core/fixtures/initial_data.json

# 7. Créer un superutilisateur admin
python3 manage.py createsuperuser

# 8. Collecter les fichiers statiques
python3 manage.py collectstatic

# 9. Lancer le serveur
python3 manage.py runserver
```

Accéder au site : http://localhost:8000
Accéder à l'admin : http://localhost:8000/admin

## Structure du projet

```
portfolio/
├── core/                    # Application principale
│   ├── fixtures/            # Données de test
│   ├── static/
│   │   ├── css/style.css    # Styles complets
│   │   └── js/
│   │       ├── particles.js # Effet particules hero
│   │       └── main.js      # Logique principale
│   ├── templates/core/
│   │   ├── index.html       # Page principale (one-page)
│   │   └── 404.html         # Page d'erreur 404
│   ├── admin.py             # Admin personnalisé
│   ├── models.py            # Modèles de données
│   ├── views.py             # Vues + API contact
│   └── urls.py              # URLs
├── portfolio/               # Configuration Django
├── media/                   # Fichiers uploadés
├── .env.example             # Template de configuration
├── requirements.txt
└── README.md
```

## Fonctionnalités

- **One-page** avec navigation fluide et highlight actif
- **Mode sombre/clair** avec persistance localStorage
- **Particules interactives** sur le hero (canvas JS, réactif à la souris)
- **Texte typé animé** dans le hero
- **Barres de progression** animées au scroll pour les compétences
- **Slider témoignages** automatique avec dots
- **Formulaire de contact** AJAX avec validation front + back
- **Loader animé** au chargement de page
- **Responsive** mobile-first
- **Admin Django** complet pour gérer tout sans code

## Configuration email (Gmail)

1. Activer la validation en 2 étapes sur votre compte Google
2. Générer un "Mot de passe d'application" dans les paramètres sécurité
3. Remplir `EMAIL_HOST_USER` et `EMAIL_HOST_PASSWORD` dans `.env`
4. Changer `EMAIL_BACKEND` en `django.core.mail.backends.smtp.EmailBackend`

## Gestion via l'admin

Aller sur `/admin/` pour :
- **SiteConfig** : nom, photo, bio, liens sociaux, CV
- **Projects** : ajouter/modifier/réordonner les projets
- **Skills** : gérer les compétences par catégorie
- **Services** : configurer les services proposés
- **Testimonials** : valider et afficher les témoignages
- **ContactMessage** : lire les messages reçus

## Déploiement production

```bash
# Dans .env
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DB_ENGINE=django.db.backends.postgresql
# ... autres variables

# Commandes
python3 manage.py collectstatic --noinput
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
```
