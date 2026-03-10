# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from decouple import config

# --- 1. CHEMINS DE BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent
# Permet de trouver les apps dans le dossier racine ou le dossier 'apps'
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# --- 2. SÉCURITÉ & ENVIRONNEMENT ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-votre-cle-de-secours')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
if 'stockpro-1-cuxp.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('stockpro-1-cuxp.onrender.com')

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

# --- 3. APPLICATIONS ---
INSTALLED_APPS = [
    'jazzmin',  # Interface admin (doit être avant admin)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Extensions tierces
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'import_export',
    'django_filters',
    'django_extensions',
    'django_prometheus',
    'debug_toolbar',  # AJOUTÉ ICI pour corriger l'erreur RuntimeError
    
    # Vos applications locales
    'accounts',
    'inventory', 
    'personnel',
    'reports',
]

# --- 4. MIDDLEWARE ---
MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# Activation de la Debug Toolbar uniquement en local
if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'stockpro.urls'

# --- 5. TEMPLATES ---
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

WSGI_APPLICATION = 'stockpro.wsgi.application'

# --- 6. BASE DE DONNÉES (LOGIQUE RENDER VS LOCAL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

if RENDER_EXTERNAL_HOSTNAME:
    # Chemin vers le disque persistant sur Render
    if os.path.exists('/var/lib/stockpro'):
        DATABASES['default']['NAME'] = '/var/lib/stockpro/db.sqlite3'
    else:
        DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
else:
    # Chemin local
    DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')

# --- 7. INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# --- 8. FICHIERS STATIQUES ET MÉDIAS ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuration WhiteNoise pour éviter les erreurs de build sur Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False 

MEDIA_URL = '/media/'
if RENDER_EXTERNAL_HOSTNAME and os.path.exists('/var/lib/stockpro'):
    MEDIA_ROOT = '/var/lib/stockpro/media'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- 9. SÉCURITÉ HTTPS (PRODUCTION) ---
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = ['https://stockpro-1-cuxp.onrender.com']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- 10. JAZZMIN SETTINGS ---
JAZZMIN_SETTINGS = {
    "site_title": "StockPro Admin",
    "site_header": "StockPro",
    "site_brand": "StockPro Management",
    "show_sidebar": True,
    "theme": "flatly",
    "changeform_format": "horizontal_tabs",
}

# --- 11. AUTRES CONFIGURATIONS ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = 'inventory:dashboard'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'