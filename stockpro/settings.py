import os
import sys
from pathlib import Path
from decouple import config

# 1. Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 2. Sécurité
SECRET_KEY = config('SECRET_KEY', default='django-insecure-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# 3. Définition des Applications
INSTALLED_APPS = [
    'jazzmin',  # Toujours en premier
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
    'debug_toolbar',
    'django_extensions',
    
    # Locaux
    'accounts',
    'inventory', 
    'personnel',
    'reports',
]

# 4. Middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware', # Debug toolbar en haut
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 8. Statiques (Vérifiez bien ces chemins !)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'inventory:dashboard'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INTERNAL_IPS = ['127.0.0.1']

# --- CONFIGURATION JAZZMIN RADICALE (Anti-blocage) ---
JAZZMIN_SETTINGS = {
    "site_title": "StockPro Admin",
    "site_header": "StockPro",
    "site_brand": "StockPro Management",
    "welcome_sign": "Bienvenue sur StockPro",
    "copyright": "StockPro Ltd",
    "search_model": ["auth.User", "inventory.Item"],
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # ICI EST LA CORRECTION : 
    # On force le format "single" (une seule page sans onglets) pour l'utilisateur
    # pour éviter que le JavaScript ne bloque l'affichage.
    "changeform_format": "horizontal_tabs", 
    "changeform_format_overrides": {
        "auth.user": "single", # <--- FORCE TOUT LE FORMULAIRE À ÊTRE VISIBLE D'UN COUP
        "auth.group": "horizontal_tabs",
    },
    
    "icons": {
        "auth.user": "fas fa-user",
        "inventory.Item": "fas fa-boxes",
        "inventory.Movement": "fas fa-exchange-alt",
        "inventory.Category": "fas fa-tags",
        "personnel.Employee": "fas fa-users",
    },
}

JAZZMIN_UI_CONFIG = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark-primary",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "theme": "flatly", 
}