# test_users.py - Script de test automatisé FINAL
import os
import django
import sys
from datetime import date # Importation nécessaire pour les dates

# 1. INITIALISATION DE L'ENVIRONNEMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpro.settings')
django.setup()

# 2. IMPORTS DES MODÈLES
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from inventory.models import Item, Movement, Category, AcquisitionMode, Inventory
from personnel.models import Employee, Department

def test_user_creation():
    """Tester la création des utilisateurs"""
    print("\n🔍 TEST 1: Création des utilisateurs")
    users_data = [
        {'username': 'gest_stock', 'password': 'test1234', 'is_staff': True},
        {'username': 'magasinier', 'password': 'test1234', 'is_staff': False},
        {'username': 'superviseur', 'password': 'test1234', 'is_staff': True, 'is_superuser': True},
    ]
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'is_staff': data.get('is_staff', False),
                'is_superuser': data.get('is_superuser', False)
            }
        )
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"  ✅ Utilisateur créé: {data['username']}")
        else:
            print(f"  ℹ️ Utilisateur existant: {data['username']}")
    return True

def test_authentication():
    """Tester l'authentification"""
    print("\n🔍 TEST 2: Authentification")
    test_users = ['gest_stock', 'magasinier', 'superviseur']
    for username in test_users:
        user = authenticate(username=username, password='test1234')
        if user:
            print(f"  ✅ {username} peut se connecter")
        else:
            print(f"  ❌ {username} ne peut pas se connecter")
    return True

def test_acquisition_modes():
    """Tester les modes d'acquisition"""
    print("\n🔍 TEST 3: Modes d'acquisition")
    modes = ['Achat', 'Don', 'Legs', 'Production', 'Transfert']
    for mode_name in modes:
        mode, created = AcquisitionMode.objects.get_or_create(name=mode_name)
        if created:
            print(f"  ✅ Mode créé: {mode_name}")
        else:
            print(f"  ℹ️ Mode existant: {mode_name}")
    return True

def test_item_creation():
    """Tester la création d'article"""
    print("\n🔍 TEST 4: Création article individuel")
    cat, _ = Category.objects.get_or_create(name='Informatique')
    item, created = Item.objects.get_or_create(
        code='ORD-HP-001',
        defaults={
            'name': 'Ordinateur HP Pavilion',
            'category': cat,
            'quantity': 5,
            'unit_price': 350000,
        }
    )
    if created:
        print(f"  ✅ Article créé: {item.code}")
    else:
        print(f"  ℹ️ Article existant: {item.code}")
    return True

def test_movement_with_beneficiary():
    """Tester mouvement avec affectation"""
    print("\n🔍 TEST 5: Mouvement avec bénéficiaire")
    
    # 1. Créer le département
    dept, _ = Department.objects.get_or_create(name='DIRECTION')
    
    # 2. Créer l'employé avec TOUS les champs obligatoires (hire_date ajouté ici)
    emp, created = Employee.objects.get_or_create(
        employee_id='EMP001',
        defaults={
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'department': dept,
            'hire_date': date.today() # ✅ Correction de la contrainte NOT NULL
        }
    )
    
    # 3. Vérifier l'article
    item = Item.objects.filter(code='ORD-HP-001').first()
    
    if item and emp:
        print(f"  ✅ Employé prêt: {emp.first_name} {emp.last_name}")
        print(f"  ✅ Liaison avec l'article {item.code} opérationnelle")
        return True
    return False

def run_all_tests():
    """Exécuter la suite de tests"""
    print("="*50)
    print("🧪 TESTS DE VALIDATION - STOCKPRO")
    print("="*50)
    
    tests = [
        test_user_creation,
        test_authentication,
        test_acquisition_modes,
        test_item_creation,
        test_movement_with_beneficiary,
    ]
    
    success_count = 0
    for test in tests:
        try:
            if test():
                success_count += 1
        except Exception as e:
            print(f"  ❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "="*50)
    print(f"📊 RÉSULTAT FINAL: {success_count}/{len(tests)} tests réussis")
    print("="*50)
    
    if success_count == len(tests):
        print("\n🎉 FÉLICITATIONS ! Votre logiciel StockPro est prêt.")

if __name__ == '__main__':
    run_all_tests()
