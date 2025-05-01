from django.contrib import admin

from .models import RecipeImage

@admin.register(RecipeImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'recipe_image', 'created']
    list_filter = ['created']