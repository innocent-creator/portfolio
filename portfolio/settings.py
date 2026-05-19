from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production-please')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'cloudinary',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

# Base de données — DATABASE_URL prioritaire (Neon/Supabase/etc.), SQLite en fallback
_DATABASE_URL = config('DATABASE_URL', default=None)
if _DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(_DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []  # core/static/ est trouvé automatiquement via AppDirectoriesFinder

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
# Shim pour django-cloudinary-storage qui accède à STATICFILES_STORAGE (supprimé en Django 5)
STATICFILES_STORAGE = STORAGES['staticfiles']['BACKEND']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

RESEND_API_KEY = config('RESEND_API_KEY', default='')

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@portfolio.com')

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:8000', cast=Csv())
CORS_ALLOW_ALL_ORIGINS = DEBUG

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000', cast=Csv())

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.AnonRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'anon': '10/min'},
}

# ── Jazzmin ──────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "Portfolio Admin",
    "site_header": "Portfolio — Innocent ATCHA",
    "site_brand": "<AI/>",
    "site_logo": None,
    "welcome_sign": "Bienvenue dans votre espace d'administration 👋",
    "copyright": "Innocent ATCHA",
    "search_model": ["core.ContactMessage", "core.Project"],
    "topmenu_links": [
        {"name": "🌐 Voir le site",  "url": "/",                "new_window": True},
        {"name": "📨 Messages",      "model": "core.ContactMessage"},
        {"name": "🚀 Projets",       "model": "core.Project"},
    ],
    "usermenu_links": [
        {"name": "🌐 Voir le site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth"],
    "order_with_respect_to": [
        "core",
        "core.SiteConfig",
        "core.Project",
        "core.Skill",
        "core.Service",
        "core.Testimonial",
        "core.ContactMessage",
    ],
    "icons": {
        "auth":                  "fas fa-users-cog",
        "auth.user":             "fas fa-user",
        "auth.Group":            "fas fa-users",
        "core":                  "fas fa-layer-group",
        "core.SiteConfig":       "fas fa-sliders-h",
        "core.Skill":            "fas fa-code",
        "core.Project":          "fas fa-rocket",
        "core.Service":          "fas fa-briefcase",
        "core.Testimonial":      "fas fa-star",
        "core.ContactMessage":   "fas fa-envelope",
    },
    "default_icon_parents":  "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active":  True,
    "custom_css": None,
    "custom_js":  None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "core.SiteConfig": "collapsible",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":          False,
    "footer_small_text":          False,
    "body_small_text":            False,
    "brand_small_text":           False,
    "brand_colour":               "navbar-indigo",
    "accent":                     "accent-indigo",
    "navbar":                     "navbar-dark navbar-indigo",
    "no_navbar_border":           True,
    "navbar_fixed":               True,
    "layout_boxed":               False,
    "footer_fixed":               False,
    "sidebar_fixed":              True,
    "sidebar":                    "sidebar-dark-indigo",
    "sidebar_nav_small_text":     False,
    "sidebar_disable_expand":     False,
    "sidebar_nav_child_indent":   True,
    "sidebar_nav_compact_style":  True,
    "sidebar_nav_legacy_style":   False,
    "sidebar_nav_flat_style":     False,
    "theme":                      "darkly",
    "dark_mode_theme":            "darkly",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-outline-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}

# Sécurité renforcée en production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    