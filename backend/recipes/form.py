from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            ingredients = self.cleaned_data.get('ingredients')
            if not ingredients or len(ingredients) == 0:
                raise ValidationError(
                    'Рецепт должен содержать хотя бы один ингредиент'
                )
        return cleaned_data
