import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpro.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'votre_mot_de_passe_ici')
    print("Superuser created: admin")
else:
    print("Superuser already exists")