from django.contrib import admin
from .models import Category, Item, Movement, AcquisitionMode

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'quantity', 'unit_price')
    search_fields = ('code', 'name')
    list_filter = ('category',)

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    # J'ai retiré 'date' car il cause l'erreur. 
    # Si vous avez un champ de date, remplacez 'created_at' par son nom exact.
    list_display = ('item', 'quantity', 'movement_type') 
    list_filter = ('movement_type',)

@admin.register(AcquisitionMode)
class AcquisitionModeAdmin(admin.ModelAdmin):
    list_display = ('name',)
