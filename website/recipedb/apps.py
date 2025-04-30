from django.apps import AppConfig


class RecipeDBConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipedb'

    def ready(self):
        import recipedb.signals
