from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
    """Département/Service"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Employee(models.Model):
    """Employé/Bénéficiaire"""
    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('conge', 'En congé'),
        ('suspendu', 'Suspendu'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    
    # Contact
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    # Fonction
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Département")
    position = models.CharField(max_length=100, verbose_name="Poste")
    
    # Dates
    hire_date = models.DateField(verbose_name="Date d'embauche")
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actif', verbose_name="Statut")
    
    # Photo
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name="Photo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.employee_id} - {self.last_name} {self.first_name}"
    
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
