from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.template import RequestContext
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django import forms
from django.core.urlresolvers import reverse
from main.models import Recipe, Ingredient
from .forms import RecipeForm, IngredientForm

def success(request):
	
	context = {}

	request.method == 'POST'

	return render(request, 'success.html', context)

def recipe_list_API_view(request):
	recipes = Recipe.objects.all()
	output = serializers.serialize('json', recipes, fields=('name', 'ingredients', 'steps'))
	return HttpResponse(output, content_type='application/json')

def listview(request):
	recipes = Recipe.objects.all()

	context = {}

	for recipe in recipes:

		recipe.title = recipe.name

	context['recipes'] = recipes 

	return render_to_response('listview.html', context, context_instance=RequestContext(request))

def recipe_detail(request, slug):
	
	request_context = RequestContext(request)
	context = {}
	recipe = Recipe.objects.get(slug=slug)
	ingredient_list = []
	for ingredient in recipe.ingredients.all():
		ingredient_list.append(ingredient)
	context['ingredients'] = ingredient_list
	context['recipe'] = recipe 

	return render_to_response('recipe_detail.html', context, context_instance=request_context)


class RecipeCreateView(CreateView):
	form_class = RecipeForm 
	template_name = "recipe_form.html"
	slug_url_kwarg = 'slug'

class IngredientCreateView(CreateView):
	form_class = IngredientForm
	template_name = "ingred_form.html"


	





