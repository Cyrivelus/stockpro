from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Item, Movement, AcquisitionMode, Inventory, InventoryItem
from .forms import ItemForm, MovementForm, InventoryForm, InventoryItemForm, CategoryForm

# --- TABLEAU DE BORD ---
@login_required
def dashboard(request):
    return render(request, 'inventory/dashboard.html', {'title': 'Tableau de Bord'})

# --- LISTE ET DÉTAILS ---
@login_required
def item_list(request):
    items = Item.objects.all().order_by('name')
    return render(request, 'inventory/item_list.html', {
        'items': items, 
        'title': 'Inventaire Global'
    })

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'inventory/item_detail.html', {'item': item, 'title': item.name})

# --- CRÉATION ---
@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES) # Ajout de FILES pour l'image
        if form.is_valid():
            form.save()
            messages.success(request, "L'article a été créé avec succès.")
            return redirect('inventory:item_list')
    else:
        form = ItemForm()
    
    return render(request, 'inventory/item_form.html', {
        'form': form, 
        'title': 'Nouvel Article'
    })

# --- MODIFICATION ---
@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        # L'instance=item est CRUCIAL pour modifier et non créer un doublon
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'article '{item.name}' a été mis à jour.")
            return redirect('inventory:item_list')
    else:
        # On pré-remplit le formulaire avec les données de l'article
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/item_form.html', {
        'form': form, 
        'item': item,
        'title': 'Modifier Article'
    })

# --- SUPPRESSION ---
@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Article supprimé définitivement.")
        return redirect('inventory:item_list')
    return render(request, 'inventory/item_confirm_delete.html', {
        'item': item,
        'title': 'Confirmer la suppression'
    })

# --- MOUVEMENTS ---
@login_required
def movement_list(request):
    movements = Movement.objects.all().order_by('-created_at') # Vérifiez le nom du champ date dans votre modèle
    return render(request, 'inventory/movement_list.html', {
        'movements': movements, 
        'title': 'Mouvements de Stock'
    })