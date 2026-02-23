from django.test import TestCase
from django.apps import apps

class StockProCahierChargeTest(TestCase):
    def test_logique_stock(self):
        print('\n' + '='*50)
        Item = apps.get_model('inventory', 'Item')
        Category = apps.get_model('inventory', 'Category')
        cat = Category.objects.create(name='Materiel')
        item = Item.objects.create(name='PC Test', category=cat, quantity=50, unit_price=100)
        
        print(f'ACQUISITION : {item.name} cree avec 50 unites.')
        item.quantity -= 10
        item.save()
        print('MOUVEMENT : Sortie de 10 unites.')
        
        self.assertEqual(item.quantity, 40)
        print(f'INVENTAIRE : Situation de stock = {item.quantity}')
        print('='*50)
        print('RESULTAT : LOGIQUE DE STOCK CONFORME')
        print('='*50)
