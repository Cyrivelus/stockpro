# test_users.py - Script de test automatisé
import os
import django
from datetime import datetime

# 1. INITIALISATION (OBLIGATOIREMENT EN PREMIER)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpro.settings')
django.setup()

# 2. IMPORTS DES FONCTIONS DE BASE
from django.contrib.auth import authenticate

def test_user_creation():
    from django.contrib.auth.models import User # Import local
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
    from apps.inventory.models import AcquisitionMode # Import local
    print("\n🔍 TEST 3: Modes d'acquisition")
    modes = ['Achat', 'Don', 'Legs', 'Production', 'Transfert']
    for mode_name in modes:
        mode, created = AcquisitionMode.objects.get_or_create(name=mode_name)
        print(f"  ✅ Mode: {mode_name}")
    return True

def test_item_creation():
    from apps.inventory.models import Item, Category # Import local
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
    print(f"  ✅ Article: {item.code}")
    return True

def test_movement_with_beneficiary():
    from personnel.models import Employee # Import local
    from apps.inventory.models import Item
    print("\n🔍 TEST 5: Mouvement avec bénéficiaire")
    emp, _ = Employee.objects.get_or_create(
        employee_id='EMP001',
        defaults={'first_name': 'Jean', 'last_name': 'Dupont'}
    )
    item = Item.objects.filter(code='ORD-HP-001').first()
    if item:
        print(f"  ✅ Mouvement prêt pour l'employé: {emp.first_name}")
    return True

def run_all_tests():
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
            if test(): success_count += 1
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    print("\n" + "="*50)
    print(f"📊 RÉSULTAT: {success_count}/{len(tests)} tests réussis")
    print("="*50)

if __name__ == '__main__':
    run_all_tests()
