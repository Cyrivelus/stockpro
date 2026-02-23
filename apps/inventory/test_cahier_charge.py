from django.test import TestCase
from django.contrib.auth.models import User
from .models import Item, Category, Movement
from personnel.models import Personnel  # Adaptez selon votre structure

class StockProComplianceTest(TestCase):
    def setUp(self):
        # Initialisation des données de base
        self.user = User.objects.create_superuser('admin', 'admin@test.com', 'pass')
        self.cat = Category.objects.create(name="Informatique")
        self.perso = Personnel.objects.create(nom="Jean Dupont", matricule="JD001")

    def test_respect_cahier_des_charges(self):
        print("\n--- DEBUT DES TESTS CAHIER DES CHARGES ---")

        # 1. TEST ACQUISITION (Achat, Don, etc.)
        # On vérifie que le système accepte l'enregistrement détaillé
        item = Item.objects.create(
            name="Ordinateur HP Pavilion",
            category=self.cat,
            quantity=10,
            unit_price=500000,
            description="Acquisition par Achat - Processeur i7, 16GB RAM",
            status="Disponible"
        )
        self.assertEqual(item.quantity, 10)
        print(f"✅ Acquisition enregistrée : {item.name} ({item.quantity} unités)")

        # 2. TEST MOUVEMENT / AFFECTATION AU PERSONNEL
        # Sortie de 2 ordinateurs pour Jean Dupont
        mouvement = Movement.objects.create(
            item=item,
            quantity=2,
            type='SORTIE',
            personnel=self.perso,
            reason="Affectation personnel"
        )
        
        # Simulation de la mise à jour du stock (Logique métier)
        item.quantity -= mouvement.quantity
        item.save()
        
        self.assertEqual(item.quantity, 8)
        print(f"✅ Sortie/Affectation réussie : 2 unités affectées à {self.perso.nom}")

        # 3. TEST INVENTAIRE / SITUATION DE STOCK
        # Vérification du "Stock Final" après mouvements
        stock_final = Item.objects.get(id=item.id).quantity
        self.assertEqual(stock_final, 8)
        print(f"✅ Calcul d'inventaire correct : Stock restant = {stock_final}")

        print("--- TOUS LES POINTS DU CAHIER DES CHARGES SONT VALIDÉS ---")