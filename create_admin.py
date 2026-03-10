import os
import django
import sys

# On s'assure que le dossier racine est dans le path pour trouver 'stockpro'
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpro.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    username = 'tamboug'
    email = 'admin@example.com'
    password = 'aaaAAA123'

    if not User.objects.filter(username=username).exists():
        # Utilisation de create_superuser pour garantir tous les droits
        User.objects.create_superuser(username, email, password)
        print(f"SUCCÈS : L'administrateur '{username}' a été créé.")
    else:
        print(f"INFO : L'utilisateur '{username}' existe déjà. Pas de création nécessaire.")

if __name__ == "__main__":
    try:
        create_superuser()
    except Exception as e:
        print(f"ERREUR lors de la création de l'admin : {e}")
        # On ne fait pas sys.exit(1) ici pour ne pas empêcher 
        # Gunicorn de démarrer si seule la création d'admin échoue.