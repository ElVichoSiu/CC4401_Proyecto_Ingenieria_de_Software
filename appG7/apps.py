from django.apps import AppConfig


class Appg7Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appG7'
    def ready(self):
        print("Importing signals...")  # Esta línea imprimirá un mensaje cuando se importen las señales
        import appG7.signals
