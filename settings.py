# -*- coding: utf-8 -*-
import os
from pathlib import Path

# --- CHEMINS DE BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SÉCURITÉ ---
# On utilise une variable d'environnement pour basculer DEBUG automatiquement
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Indispensable pour supprimer l'erreur DisallowedHost
ALLOWED_HOSTS = [
    'stockpro-1-cuxp.onrender.com', 
    '127.0.0.1', 
    'localhost'
]

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-votre-cle-par-defaut')

# --- CONFIGURATION DU DISQUE PERSISTANT (RENDER) ---
# On détecte si on est sur Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    # Chemin vers le Mount Path défini dans l'onglet Disk de Render
    PERSISTENT_STORAGE_ROOT = '/var/lib/stockpro'
else:
    # Chemin local pour le développement
    PERSISTENT_STORAGE_ROOT = BASE_DIR

# --- APPLICATIONS ---
INSTALLED_APPS = [
    'jazzmin',  
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
    
    # Vos applications
    'accounts',
    'inventory',
    'personnel',
    'reports',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Gestion des fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'stockpro.urls'

# --- BASE DE DONNÉES (Liaison au Disque Persistant) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PERSISTENT_STORAGE_ROOT, 'db.sqlite3'),
    }
}

# --- STATICS & MÉDIAS ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Stockage statique optimisé
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Médias liés au Disque Persistant (Photos produits)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PERSISTENT_STORAGE_ROOT, 'media')

# --- CONFIGURATION SÉCURITÉ HTTPS & CSRF ---
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = ['https://stockpro-1-cuxp.onrender.com']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True