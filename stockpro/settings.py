# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from decouple import config

# --- 1. CHEMINS DE BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# --- 2. SÉCURITÉ & ENVIRONNEMENT ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-votre-cle-de-secours')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
if 'stockpro-1-cuxp.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('stockpro-1-cuxp.onrender.com')

# --- 3. CONFIGURATION DU DISQUE PERSISTANT (RENDER) ---
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    PERSISTENT_STORAGE_ROOT = '/var/lib/stockpro'
else:
    PERSISTENT_STORAGE_ROOT = BASE_DIR

# --- 4. APPLICATIONS ---
INSTALLED_APPS = [
    'jazzmin',  # Doit rester en haut
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Tierces
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'import_export',
    'django_filters',
    'django_extensions',
    'django_prometheus',
    'debug_toolbar',
    
    # Vos apps
    'accounts',
    'inventory', 
    'personnel',
    'reports',
]

# --- 5. MIDDLEWARE ---
MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Gestion statique
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'stockpro.urls'

# --- 6. TEMPLATES ---
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

# --- 7. BASE DE DONNÉES ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PERSISTENT_STORAGE_ROOT, 'db.sqlite3'),
    }
}

# --- 8. INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- 9. STATIQUES & MÉDIAS ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Vérifiez que le dossier 'static' existe à la racine C:\xampp\htdocs\stockpro\static
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# CORRECTION CRUCIALE : On retire "Manifest" pour éviter le crash sur les fichiers .map manquants
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PERSISTENT_STORAGE_ROOT, 'media')

# --- 10. SÉCURITÉ HTTPS (PROD) ---
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = ['https://stockpro-1-cuxp.onrender.com']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- 11. CONFIGURATION JAZZMIN ---
JAZZMIN_SETTINGS = {
    "site_title": "StockPro Admin",
    "site_header": "StockPro",
    "site_brand": "StockPro Management",
    "welcome_sign": "Bienvenue sur StockPro",
    "copyright": "StockPro Ltd",
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs", 
    "changeform_format_overrides": {
        "auth.user": "single",
    },
}

JAZZMIN_UI_CONFIG = {
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "theme": "flatly", 
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'inventory:dashboard'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INTERNAL_IPS = ['127.0.0.1']