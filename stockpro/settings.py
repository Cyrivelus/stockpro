import os
import sys
from pathlib import Path
from decouple import config

# 1. Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent

# AJOUT CRUCIAL : Permet d'importer les apps directement (ex: 'inventory' au lieu de 'apps.inventory')
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 2. Sécurité
SECRET_KEY = config('SECRET_KEY', default='django-insecure-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# 3. Définition des Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'import_export',
    'django_filters',
    'debug_toolbar',
    'django_extensions',
    
    # Local apps (On utilise le nom direct car on a ajouté 'apps' au sys.path)
    'accounts',
    'inventory',
    'personnel',
    'reports',
]

# 4. Middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware', # Toujours en haut ou presque
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stockpro.urls'

# 5. Templates
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
                'django.contrib.messages.context_processors.messages', # <--- CORRIGÉ ICI
            ],
        },
    },
]

WSGI_APPLICATION = 'stockpro.wsgi.application'

# 6. Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. Internationalisation (Adapté au Cameroun)
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# 8. Fichiers Statiques et Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 9. Configuration Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# 10. Authentification
LOGIN_URL = 'login' # Ou 'accounts:login' si vous utilisez les namespaces
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 11. Debug Toolbar
INTERNAL_IPS = ['127.0.0.1']