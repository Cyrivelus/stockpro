from django.db import models
from django.core.exceptions import ValidationError

# --- MODÈLES DE BASE ---

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class AcquisitionMode(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)  # Stock actuel
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Disponible")

    def __str__(self):
        return f"{self.name} ({self.quantity})"

# --- LOGIQUE DE MOUVEMENTS ---

class Movement(models.Model):
    TYPES = [('ENTREE', 'Entree'), ('SORTIE', 'Sortie')]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='movements')
    type_mouvement = models.CharField(max_length=10, choices=TYPES)
    quantite = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    # Liaison avec votre app personnel
    beneficiary = models.ForeignKey(
        'personnel.Employee', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def clean(self):
        """Bloque la validation si la sortie dépasse le stock disponible"""
        if self.type_mouvement == 'SORTIE':
            if self.quantite > self.item.quantity:
                raise ValidationError({
                    'quantite': f"Action impossible : Il ne reste que {self.item.quantity} unités en stock pour '{self.item.name}'."
                })

    def save(self, *args, **kwargs):
        # 1. On valide d'abord (clean)
        self.full_clean()
        
        # 2. Mise à jour dynamique de la quantité de l'Article
        if self.type_mouvement == 'ENTREE':
            self.item.quantity += self.quantite
        elif self.type_mouvement == 'SORTIE':
            self.item.quantity -= self.quantite
        
        # Sauvegarde de l'article avec son nouveau stock
        self.item.save()
        
        # 3. Sauvegarde du mouvement
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_mouvement} : {self.item.name} ({self.quantite})"

# --- INVENTAIRE PHYSIQUE ---

class Inventory(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Inventaires"

    def __str__(self):
        return f"Inventaire du {self.date.strftime('%d/%m/%Y')}"

class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    expected_quantity = models.IntegerField() # Quantité théorique (système)
    actual_quantity = models.IntegerField()   # Quantité réelle (comptée)

    def __str__(self):
        return f"{self.item.name} - Écart: {self.actual_quantity - self.expected_quantity}"