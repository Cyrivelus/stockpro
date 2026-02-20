from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Tableau de bord (Page d'accueil de l'inventaire)
    path('', views.dashboard, name='dashboard'),

    # Gestion des Articles (Items)
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/update/', views.item_update, name='item_update'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),

    # Gestion des Mouvements (Entrées/Sorties)
    path('movements/', views.movement_list, name='movement_list'),
    # path('movements/create/', views.movement_create, name='movement_create'), # À décommenter si la vue existe

    # Gestion des Inventaires
    # path('inventories/', views.inventory_list, name='inventory_list'), # À décommenter si la vue existe
]
