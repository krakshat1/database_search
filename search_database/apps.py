from django.apps import AppConfig


class SearchDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_database'
    
    def ready(self):
        from . import startup_script
        startup_script.run()