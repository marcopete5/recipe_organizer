from django.contrib import admin
from models import *

class IngredientAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ['name']

class RecipeAdmin(admin.ModelAdmin):
	list_display = ('name','website')
	search_fields = ['name']

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
