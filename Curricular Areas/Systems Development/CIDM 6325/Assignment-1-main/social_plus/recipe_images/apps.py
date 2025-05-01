from django.apps import AppConfig


class RecipeImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe_images'

    def ready(self):
        # import signal handlers
        import recipe_images.signals