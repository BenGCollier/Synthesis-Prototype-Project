import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import RecipeImage

    
class RecipeImageCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeImage
        fields = ['title', 'url', 'ingredients', 'instructions', 'link']
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.'
            )
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        recipe_image = super().save(commit=False)
        recipe_image_url = self.cleaned_data['url']
        name = slugify(recipe_image.title)
        extension = recipe_image_url.rsplit('.', 1)[1].lower()
        recipe_image_name = f'{name}.{extension}'
        # download recipe_image from the given URL
        response = requests.get(recipe_image_url)
        recipe_image.recipe_image.save(
            recipe_image_name,
            ContentFile(response.content),
            save=False
        )
        if commit:
            recipe_image.save()
        return recipe_image