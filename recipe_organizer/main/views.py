from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import CreateView
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


def tabview(request):
	recipes = Recipe.objects.all()

	context = {}

	for recipe in recipes:

		recipe.title = recipe.name

	context['recipes'] = recipes 

	return render_to_response('tabview.html', context, context_instance=RequestContext(request))

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

def recipe_full(request, slug):
	
	request_context = RequestContext(request)
	context = {}
	recipe = Recipe.objects.get(slug=slug)
	ingredient_list = []
	for ingredient in recipe.ingredients.all():
		ingredient_list.append(ingredient)
	context['ingredients'] = ingredient_list
	context['recipe'] = recipe 

	return render_to_response('recipe_full.html', context, context_instance=request_context)

def home_slider(request):

	context = {}
	recipes = []
	for x in range(4):
		random_recipe = Recipe.objects.all().order_by('?')[1]
		
		recipes.append(random_recipe)
	
	context["recipes"] = recipes

	return render(request, 'home.html', context)






		
import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
	request_context = RequestContext(request)
	context = {}
	recipe = Recipe.objects.all()
	ingredient_list = []
	query_string = ''
    
	for ingredient in recipe:
		ingredient_list.append(ingredient)
	context['ingredients'] = ingredient_list
	context['recipe'] = recipe 


	if ('q' in request.GET) and request.GET['q'].strip():
	        query_string = request.GET['q']
	        
	        ingredients = get_query(query_string, ['name'])
	        
	        found_entries = Ingredient.objects.filter(ingredients)
	        print type(found_entries)

	        recipes = []
	        for entries in found_entries:
	        	print dir(entries)
	        	recipes.append(Recipe.objects.filter(ingredients=entries.pk))

	        found_entries = recipes 


	return render_to_response('search.html',{ 'query_string': query_string, 'found_entries': found_entries }, context_instance=RequestContext(request))

	





