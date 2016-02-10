from django import forms
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ['name', 'steps', 'image', 'website']
		labels = {
			'name': ('Recipe Name'), 'steps': ('Instructions'), 'website':('Recipe Website (optional)')
		}

class IngredientForm (forms.ModelForm):
	class Meta:
		model = Ingredient 
		fields = ['name']
