from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import csv
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .models import (
    Category, Supplier, Item, Movement, 
    AcquisitionMode, Inventory, InventoryItem
)
from apps.personnel.models import Employee
from .forms import (
    ItemForm, MovementForm, InventoryForm,
    InventoryItemForm, CategoryForm, SupplierForm
)

@login_required
def dashboard(request):
    """Tableau de bord principal"""
    context = {}
    
    # Statistiques générales
    context['total_items'] = Item.objects.count()
    context['total_value'] = Item.objects.aggregate(total=Sum('total_value'))['total'] or 0
    context['low_stock'] = Item.objects.filter(quantity__lte=models.F('min_stock')).count()
    context['total_movements'] = Movement.objects.count()
    
    # Derniers mouvements
    context['recent_movements'] = Movement.objects.select_related('item', 'beneficiary').order_by('-movement_date')[:10]
    
    # Articles en stock critique
    context['critical_items'] = Item.objects.filter(quantity__lte=models.F('min_stock')).order_by('quantity')[:10]
    
    # Statistiques par catégorie
    context['category_stats'] = Category.objects.annotate(
        item_count=Count('item'),
        total_value=Sum('item__total_value')
    ).filter(item_count__gt=0)
    
    # Graphique des mouvements (30 derniers jours)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    movements = Movement.objects.filter(
        movement_date__range=[start_date, end_date]
    ).extra({'date': "date(movement_date)"}).values('date').annotate(
        entries=Sum('quantity', filter=Q(movement_type='entree')),
        exits=Sum('quantity', filter=Q(movement_type='sortie'))
    ).order_by('date')
    
    context['chart_labels'] = [m['date'] for m in movements]
    context['chart_entries'] = [float(m['entries'] or 0) for m in movements]
    context['chart_exits'] = [float(m['exits'] or 0) for m in movements]
    
    return render(request, 'inventory/dashboard.html', context)

# ========== GESTION DES ARTICLES ==========

@login_required
def item_list(request):
    """Liste des articles"""
    items = Item.objects.select_related('category').all()
    
    # Filtres
    category = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    if category:
        items = items.filter(category_id=category)
    if status:
        items = items.filter(status=status)
    if search:
        items = items.filter(
            Q(code__icontains=search) |
            Q(name__icontains=search) |
            Q(serial_number__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'status_choices': Item.STATUS_CHOICES,
        'current_category': category,
        'current_status': status,
        'current_search': search,
    }
    return render(request, 'inventory/item_list.html', context)

@login_required
def item_detail(request, pk):
    """Détail d'un article"""
    item = get_object_or_404(Item.objects.select_related('category'), pk=pk)
    movements = item.movement_set.select_related('beneficiary').order_by('-movement_date')[:20]
    
    context = {
        'item': item,
        'movements': movements,
    }
    return render(request, 'inventory/item_detail.html', context)

@login_required
def item_create(request):
    """Créer un nouvel article"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, f"Article {item.code} créé avec succès.")
            return redirect('inventory:item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    return render(request, 'inventory/item_form.html', {'form': form, 'title': 'Nouvel Article'})

@login_required
def item_update(request, pk):
    """Modifier un article"""
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Article {item.code} modifié avec succès.")
            return redirect('inventory:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/item_form.html', {'form': form, 'title': 'Modifier Article'})

@login_required
def item_delete(request, pk):
    """Supprimer un article"""
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f"Article {item.code} supprimé.")
        return redirect('inventory:item_list')
    
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

# ========== GESTION DES MOUVEMENTS ==========

@login_required
def movement_list(request):
    """Liste des mouvements"""
    movements = Movement.objects.select_related('item', 'beneficiary', 'supplier').order_by('-movement_date')
    
    # Filtres
    movement_type = request.GET.get('type')
    item = request.GET.get('item')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    if item:
        movements = movements.filter(item_id=item)
    if start_date:
        movements = movements.filter(movement_date__date__gte=start_date)
    if end_date:
        movements = movements.filter(movement_date__date__lte=end_date)
    
    # Pagination
    paginator = Paginator(movements, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'items': Item.objects.all(),
        'movement_types': Movement.MOVEMENT_TYPES,
        'current_type': movement_type,
        'current_item': item,
        'current_start': start_date,
        'current_end': end_date,
    }
    return render(request, 'inventory/movement_list.html', context)

@login_required
def movement_create(request):
    """Créer un mouvement (entrée/sortie)"""
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.created_by = request.user
            movement.save()
            
            # Message selon le type
            if movement.movement_type == 'entree':
                msg = f"Entrée en stock de {movement.quantity} {movement.item.name}"
            else:
                if movement.beneficiary:
                    msg = f"Sortie de {movement.quantity} {movement.item.name} pour {movement.beneficiary}"
                else:
                    msg = f"Sortie de {movement.quantity} {movement.item.name}"
            
            messages.success(request, msg)
            return redirect('inventory:movement_list')
    else:
        # Pré-remplir avec les paramètres GET
        initial = {}
        if request.GET.get('item'):
            initial['item'] = request.GET.get('item')
        if request.GET.get('type'):
            initial['movement_type'] = request.GET.get('type')
        form = MovementForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Nouveau Mouvement',
        'items': Item.objects.filter(status='disponible')
    }
    return render(request, 'inventory/movement_form.html', context)

# ========== INVENTAIRES ==========

@login_required
def inventory_list(request):
    """Liste des inventaires"""
    inventories = Inventory.objects.all().order_by('-date')
    
    context = {
        'inventories': inventories,
    }
    return render(request, 'inventory/inventory_list.html', context)

@login_required
def inventory_create(request):
    """Créer un nouvel inventaire"""
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user
            inventory.save()
            
            # Créer les lignes d'inventaire pour tous les articles
            for item in Item.objects.all():
                InventoryItem.objects.create(
                    inventory=inventory,
                    item=item,
                    actual_quantity=item.quantity,
                    theoretical_quantity=item.quantity
                )
            
            messages.success(request, f"Inventaire {inventory.name} créé. Veuillez saisir les quantités réelles.")
            return redirect('inventory:inventory_edit', pk=inventory.pk)
    else:
        form = InventoryForm()
    
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Nouvel Inventaire'})

@login_required
def inventory_detail(request, pk):
    """Détail d'un inventaire"""
    inventory = get_object_or_404(Inventory, pk=pk)
    items = inventory.items.select_related('item').all()
    
    context = {
        'inventory': inventory,
        'items': items,
    }
    return render(request, 'inventory/inventory_detail.html', context)

@login_required
def inventory_edit(request, pk):
    """Saisie des quantités réelles"""
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('actual_'):
                item_id = key.replace('actual_', '')
                try:
                    inventory_item = InventoryItem.objects.get(
                        inventory=inventory,
                        item_id=item_id
                    )
                    inventory_item.actual_quantity = int(value)
                    inventory_item.save()
                except:
                    pass
        
        # Mettre à jour les totaux
        inventory.total_items = inventory.items.count()
        inventory.total_value = inventory.items.aggregate(
            total=Sum('actual_value')
        )['total'] or 0
        inventory.status = 'termine'
        inventory.save()
        
        messages.success(request, "Inventaire mis à jour.")
        return redirect('inventory:inventory_detail', pk=inventory.pk)
    
    items = inventory.items.select_related('item').all()
    
    return render(request, 'inventory/inventory_edit.html', {
        'inventory': inventory,
        'items': items
    })

# ========== RAPPORTS ==========

@login_required
def reports_index(request):
    """Page des rapports"""
    return render(request, 'reports/index.html')

@login_required
def export_stock_csv(request):
    """Exporter l'état du stock en CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="etat_stock.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Code', 'Nom', 'Catégorie', 'Quantité', 'Prix Unitaire', 'Valeur Totale', 'Statut'])
    
    for item in Item.objects.select_related('category').all():
        writer.writerow([
            item.code,
            item.name,
            item.category.name,
            item.quantity,
            item.unit_price,
            item.total_value,
            item.get_status_display(),
        ])
    
    return response

@login_required
def export_stock_excel(request):
    """Exporter l'état du stock en Excel"""
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="etat_stock.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('État du Stock')
    
    # En-têtes
    headers = ['Code', 'Nom', 'Catégorie', 'Quantité', 'Prix Unitaire', 'Valeur Totale', 'Statut']
    for col, header in enumerate(headers):
        ws.write(0, col, header, xlwt.easyxf('font: bold on'))
    
    # Données
    for row, item in enumerate(Item.objects.select_related('category').all(), start=1):
        ws.write(row, 0, item.code)
        ws.write(row, 1, item.name)
        ws.write(row, 2, item.category.name)
        ws.write(row, 3, item.quantity)
        ws.write(row, 4, float(item.unit_price))
        ws.write(row, 5, float(item.total_value))
        ws.write(row, 6, item.get_status_display())
    
    wb.save(response)
    return response

@login_required
def export_stock_pdf(request):
    """Exporter l'état du stock en PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etat_stock.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    
    # Titre
    styles = getSampleStyleSheet()
    title = Paragraph("État du Stock", styles['Title'])
    elements.append(title)
    
    # Date
    date = Paragraph(f"Généré le: {timezone.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
    elements.append(date)
    
    # Tableau
    data = [['Code', 'Nom', 'Catégorie', 'Qté', 'Prix U.', 'Valeur']]
    for item in Item.objects.select_related('category').all()[:50]:  # Limite pour le PDF
        data.append([
            item.code,
            item.name[:30],
            item.category.name,
            str(item.quantity),
            f"{item.unit_price:,.0f} FCFA",
            f"{item.total_value:,.0f} FCFA"
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response