from django import forms
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ['name', 'steps', 'image', 'website']

class IngredientForm (forms.ModelForm):
	class Meta:
		model = Ingredient 
		fields = ['name']
