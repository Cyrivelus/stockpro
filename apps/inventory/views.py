from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
@login_required
def dashboard(request):
    return render(request, 'inventory/dashboard.html', {'title': 'Tableau de Bord'})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

# Imports relatifs (le point signifie "dans ce dossier")
from .models import Category, Item, Movement, AcquisitionMode, Inventory, InventoryItem
from .forms import ItemForm, MovementForm, InventoryForm, InventoryItemForm, CategoryForm

# Import de l'autre application (chemin complet)
try:
    from personnel.models import Employee
except ImportError:
    from personnel.models import Employee

@login_required
def item_list(request):
    return render(request, 'inventory/item_list.html', {'title': 'Liste des articles'})

@login_required
def item_detail(request, pk):
    return render(request, 'inventory/item_detail.html', {'title': 'Detail Article'})

@login_required
def movement_list(request):
    return render(request, 'inventory/movement_list.html', {'title': 'Mouvements'})

@login_required
def item_create(request):
    return render(request, 'inventory/item_form.html', {'title': 'Nouvel Article'})

@login_required
def item_update(request, pk):
    return render(request, 'inventory/item_form.html', {'title': 'Modifier Article'})

@login_required
def item_delete(request, pk):
    return render(request, 'inventory/item_confirm_delete.html', {'title': 'Supprimer Article'})

from django.shortcuts import render, redirect
from .models import Item
# Assurez-vous d'importer les formulaires si vous en avez un, 
# sinon nous allons utiliser une méthode simple ici.

@login_required
def item_create(request):
    if request.method == "POST":
        # Récupération simple des données du formulaire
        designation = request.POST.get('designation')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        
        # Création de l'article en base de données
        Item.objects.create(
            designation=designation,
            quantity=quantity
            # Ajoutez les autres champs selon votre modèle Item
        )
        return redirect('inventory:item_list')
        
    return render(request, 'inventory/item_form.html', {'title': 'Nouvel Article'})