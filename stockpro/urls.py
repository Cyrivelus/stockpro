from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

# Change le titre dans l'onglet du navigateur (ex: "Gestion de Stock | Admin")
admin.site.site_title = "StockPro Admin"

# Change le texte dans l'en-tête bleu de l'interface admin
admin.site.site_header = "StockPro - Administration de l'Inventaire"

# Change le texte sur la page de connexion et le titre de l'index
admin.site.index_title = "Tableau de bord de gestion"

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),
    
    # Authentification (login, logout, password_reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Application Inventaire (Racine du site)
    path('', include('apps.inventory.urls')),
    
    # Autres Applications (SANS le préfixe "apps.")
    path('personnel/', include('personnel.urls')),
    path('reports/', include('reports.urls')),
]

# Configuration pour le développement (Debug Toolbar et Fichiers Media/Static)
if settings.DEBUG:
    # Debug Toolbar
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    
    # Servir les fichiers médias et statiques en local
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
