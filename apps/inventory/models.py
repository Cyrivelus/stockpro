from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

class Category(models.Model):
    """Catégorie d'articles"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    """Fournisseur"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="Personne de contact")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    website = models.URLField(blank=True, verbose_name="Site web")
    tax_id = models.CharField(max_length=50, blank=True, verbose_name="N° TVA")
    notes = models.TextField(blank=True, verbose_name="Notes")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class AcquisitionMode(models.Model):
    """Mode d'acquisition (achat, don, legs, etc.)"""
    name = models.CharField(max_length=50, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Mode d'acquisition"
        verbose_name_plural = "Modes d'acquisition"
    
    def __str__(self):
        return self.name

class Item(models.Model):
    """Article en stock"""
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('affecte', 'Affecté'),
        ('en_maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
        ('reforme', 'Réformé'),
    ]
    
    CONDITION_CHOICES = [
        ('neuf', 'Neuf'),
        ('bon', 'Bon état'),
        ('usage', 'Usage normal'),
        ('moyen', 'État moyen'),
        ('mauvais', 'Mauvais état'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name="Code article")
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Catégorie")
    
    # Caractéristiques
    brand = models.CharField(max_length=100, blank=True, verbose_name="Marque")
    model = models.CharField(max_length=100, blank=True, verbose_name="Modèle")
    serial_number = models.CharField(max_length=100, blank=True, verbose_name="N° de série")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='neuf', verbose_name="État")
    
    # Stock
    quantity = models.IntegerField(default=1, verbose_name="Quantité")
    min_stock = models.IntegerField(default=1, verbose_name="Stock minimum")
    location = models.CharField(max_length=100, blank=True, verbose_name="Emplacement")
    
    # Valeur
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Prix unitaire")
    total_value = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    
    # Images
    image = models.ImageField(upload_to='items/', blank=True, null=True, verbose_name="Image")
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible', verbose_name="Statut")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='items_created')
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['code', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        self.total_value = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def get_current_quantity(self):
        """Calculer la quantité actuelle basée sur les mouvements"""
        entries = self.movement_set.filter(movement_type='entree').aggregate(total=models.Sum('quantity'))['total'] or 0
        exits = self.movement_set.filter(movement_type='sortie').aggregate(total=models.Sum('quantity'))['total'] or 0
        return entries - exits

class Movement(models.Model):
    """Mouvement de stock (entrée/sortie)"""
    MOVEMENT_TYPES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Article")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES, verbose_name="Type")
    quantity = models.IntegerField(verbose_name="Quantité")
    
    # Acquisition
    acquisition_mode = models.ForeignKey('AcquisitionMode', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Mode d'acquisition")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Fournisseur")
    donor = models.CharField(max_length=200, blank=True, verbose_name="Donateur")
    source = models.CharField(max_length=200, blank=True, verbose_name="Source")
    
    # Valeur
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Prix unitaire")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    
    # Pour les sorties
    beneficiary = models.ForeignKey('personnel.Employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bénéficiaire")
    destination = models.CharField(max_length=200, blank=True, verbose_name="Destination")
    
    # Documents
    invoice_number = models.CharField(max_length=100, blank=True, verbose_name="N° facture")
    receipt_number = models.CharField(max_length=100, blank=True, verbose_name="N° bon")
    
    # Dates
    movement_date = models.DateTimeField(default=timezone.now, verbose_name="Date mouvement")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Mouvement"
        verbose_name_plural = "Mouvements"
        ordering = ['-movement_date']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.item.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Mettre à jour la quantité de l'article
        item = self.item
        if self.movement_type == 'entree':
            item.quantity += self.quantity
        else:
            item.quantity -= self.quantity
        item.save()

class Inventory(models.Model):
    """Inventaire périodique"""
    STATUS_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom")
    date = models.DateField(default=timezone.now, verbose_name="Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planifie', verbose_name="Statut")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Statistiques
    total_items = models.IntegerField(default=0, verbose_name="Total articles")
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valeur totale")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} - {self.date}"

class InventoryItem(models.Model):
    """Ligne d'inventaire"""
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Article")
    
    theoretical_quantity = models.IntegerField(verbose_name="Quantité théorique")
    actual_quantity = models.IntegerField(verbose_name="Quantité réelle")
    difference = models.IntegerField(editable=False, default=0, verbose_name="Différence")
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    theoretical_value = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    actual_value = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    value_difference = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Ligne d'inventaire"
        verbose_name_plural = "Lignes d'inventaire"
        unique_together = ['inventory', 'item']
    
    def save(self, *args, **kwargs):
        self.theoretical_quantity = self.item.quantity
        self.difference = self.actual_quantity - self.theoretical_quantity
        self.unit_price = self.item.unit_price
        self.theoretical_value = self.theoretical_quantity * self.unit_price
        self.actual_value = self.actual_quantity * self.unit_price
        self.value_difference = self.actual_value - self.theoretical_value
        super().save(*args, **kwargs)