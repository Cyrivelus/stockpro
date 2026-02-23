import csv
import json
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from datetime import timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay

# Imports pour ReportLab (Génération PDF)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .models import Category, Item, Movement, AcquisitionMode, Inventory

# --- 1. CONFIGURATION DU DASHBOARD (Page d'accueil) ---

def custom_index(self, request, extra_context=None):
    # Initialisation du contexte de base (INDISPENSABLE pour le bouton déconnexion)
    extra_context = extra_context or {}
    extra_context.update(self.each_context(request))

    # Données du Graphique (7 derniers jours)
    last_7_days = timezone.now() - timedelta(days=6)
    mouvements_data = (
        Movement.objects.filter(date__gte=last_7_days)
        .annotate(day=TruncDay('date'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )
    
    labels = [d['day'].strftime('%d/%m') for d in mouvements_data]
    counts = [d['total'] for d in mouvements_data]

    # Données des Tuiles d'Alertes
    extra_context['total_items'] = Item.objects.count()
    extra_context['critical_stock'] = Item.objects.filter(quantity__lt=10).count()
    extra_context['total_mouvements'] = Movement.objects.filter(
        date__gte=timezone.now().replace(hour=0, minute=0, second=0)
    ).count()
    
    # Injection JSON pour Chart.js
    extra_context['chart_labels'] = json.dumps(labels)
    extra_context['chart_data'] = json.dumps(counts)
    
    # Appel de l'index original avec le contexte enrichi
    return admin.sites.AdminSite.index(self, request, extra_context=extra_context)

# Application du dashboard à l'instance admin
admin.site.index = custom_index.__get__(admin.site, admin.sites.AdminSite)

# Titres de l'interface (Branding)
admin.site.site_header = "STOCKPRO - Administration"
admin.site.site_title = "Gestion de Stock"
admin.site.index_title = "Tableau de Bord Logistique"


# --- 2. ACTIONS PDF & EXPORT ---

@admin.action(description="📄 Générer Rapport Mensuel (PDF)")
def generate_monthly_report(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_mensuel_stock.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    month_name = timezone.now().strftime('%B %Y')
    elements.append(Paragraph(f"Rapport d'Activité Stock - {month_name}", styles['Title']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    data = [['Article', 'Entrées', 'Sorties', 'Stock Final', 'Valeur (CFA)']]
    for item in queryset:
        current_month = timezone.now().month
        entrees = item.movements.filter(type_mouvement='ENTREE', date__month=current_month).aggregate(Sum('quantite'))['quantite__sum'] or 0
        sorties = item.movements.filter(type_mouvement='SORTIE', date__month=current_month).aggregate(Sum('quantite'))['quantite__sum'] or 0
        valeur = item.quantity * item.unit_price
        data.append([item.name, entrees, sorties, item.quantity, f"{valeur:,.2f}"])

    table = Table(data, colWidths=[150, 70, 70, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(table)
    doc.build(elements)
    return response

@admin.action(description="📊 Exporter en Excel/CSV")
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventaire_stock.csv"'
    response.write(u'\ufeff'.encode('utf8')) 
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Catégorie', 'Quantité', 'Prix', 'Statut'])
    for obj in queryset:
        writer.writerow([obj.name, obj.category.name, obj.quantity, obj.unit_price, obj.status])
    return response

@admin.action(description="🎫 Générer Bon de Sortie (PDF)")
def generate_pdf_receipt(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bon_de_sortie.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    for obj in queryset:
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "STOCKPRO - BON DE SORTIE")
        p.setFont("Helvetica", 12)
        p.drawString(100, height - 80, f"Date : {obj.date.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(100, height - 100, f"Référence : #MOV-{obj.id}")
        p.line(100, height - 110, 500, height - 110)
        p.drawString(120, height - 160, f"Article : {obj.item.name}")
        p.drawString(120, height - 180, f"Quantité : {obj.quantite}")
        p.drawString(120, height - 200, f"Bénéficiaire : {getattr(obj, 'beneficiary', 'Non spécifié')}")
        p.rect(100, height - 380, 150, 70) 
        p.rect(350, height - 380, 150, 70) 
        p.showPage()
    p.save()
    return response


# --- 3. ADMINISTRATION DES MODÈLES ---

class MovementInline(admin.TabularInline):
    model = Movement
    extra = 1
    fields = ('type_mouvement', 'quantite', 'date')
    readonly_fields = ('date',)
    classes = ['collapse']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'colored_quantity', 'unit_price', 'status')
    list_editable = ('category', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name',)
    inlines = [MovementInline]
    actions = [export_as_csv, generate_monthly_report]

    def colored_quantity(self, obj):
        if obj.quantity <= 0:
            color, label = '#d9534f', 'RUPTURE'
        elif obj.quantity < 10:
            color, label = '#f0ad4e', f'{obj.quantity} (Bas)'
        else:
            color, label = '#5cb85c', obj.quantity
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, label)
    
    colored_quantity.short_description = 'Stock Actuel'
    colored_quantity.admin_order_field = 'quantity'

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('item', 'type_mouvement', 'quantite', 'date')
    list_filter = ('type_mouvement', 'date')
    search_fields = ('item__name',)
    actions = [generate_pdf_receipt]

admin.site.register(Category)
admin.site.register(AcquisitionMode)
admin.site.register(Inventory)