from django import forms
from .models import Item, Movement, Category, Inventory, InventoryItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = '__all__'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
