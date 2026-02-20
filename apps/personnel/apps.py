from django.apps import AppConfig

class PersonnelConfig(AppConfig):
    """
    Configuration de l'application Personnel.
    Grâce au sys.path.insert dans settings.py, le 'name' est simplement 'personnel'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personnel'
    verbose_name = 'Gestion du Personnel' # Optionnel : Nom plus joli dans l'administration
