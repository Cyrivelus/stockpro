# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = config('SECRET_KEY', default='django-insecure-votre-cle-de-secours')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
if 'stockpro-1-cuxp.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('stockpro-1-cuxp.onrender.com')

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'import_export',
    'django_filters',
    'django_extensions',
    'django_prometheus',
    'accounts',
    'inventory', 
    'personnel',
    'reports',
]

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

ROOT_URLCONF = 'stockpro.urls'

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

# --- BASE DE DONNÉES (LOGIQUE ROBUSTE) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

if RENDER_EXTERNAL_HOSTNAME:
    if os.path.exists('/var/lib/stockpro'):
        DATABASES['default']['NAME'] = '/var/lib/stockpro/db.sqlite3'
    else:
        DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
else:
    DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False 

MEDIA_URL = '/media/'
if RENDER_EXTERNAL_HOSTNAME and os.path.exists('/var/lib/stockpro'):
    MEDIA_ROOT = '/var/lib/stockpro/media'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = ['https://stockpro-1-cuxp.onrender.com']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

JAZZMIN_SETTINGS = {
    "site_title": "StockPro Admin",
    "site_header": "StockPro",
    "site_brand": "StockPro Management",
    "show_sidebar": True,
    "theme": "flatly",
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = 'inventory:dashboard'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'