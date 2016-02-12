#!/usr/bin/env python

import csv
import os
import sys
import requests
import urllib
import urllib2
import StringIO
from lxml import etree, html
from slugify import slugify
from django.core.files import File
# from pillow import image

sys.path.append("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipe_organizer.settings")
import django

django.setup()

from main.models import Recipe, Ingredient

for x in range(4,10):
	api_key = '6d2560e2dcef2fd73fc7e9476c86573e'
	param_dict = {'key': api_key, 'sort': 'r', 'page': x}
	response = requests.get('http://food2fork.com/api/search/recipes.json', params=param_dict)

	# print response
	response = response.json()
	recipes = response['recipes']

	for recipe in recipes:
		result = urllib.urlopen(recipe['source_url'])
		html = result.read()

		parser = etree.HTMLParser()
		tree = etree.parse(StringIO.StringIO(html), parser)
		if recipe['publisher'] == 'Closet Cooking':
			# with requests.Session() as session:
				
			_xpath = "html/body/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[5]/ol/li/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)

		elif recipe['publisher'] == 'All Recipes':
			_xpath = "/html/body/div[1]/div[2]/div/div[2]/section/section[3]/div/div[1]/ol[1]/li/span/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)


		elif recipe['publisher'] == 'The Pioneer Woman':
			_xpath = "//*[@id='main']/div/article/div/div[2]/div/div[4]/div[2]/div[2]/div/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)

		elif recipe['publisher'] == 'Two Peas and Their Pod':
			_xpath = "//*[@id='content']/div[1]/div[4]/div/div[4]/p/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)

		elif recipe['publisher'] == '101 Cookbooks':
			_xpath = "//*[@id='recipe']/p/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)

		elif recipe['publisher'] == 'Whats Gaby Cooking':
			_xpath = "//*[@id='zlrecipe-instructions-list']/li/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)

		elif recipe['publisher'] == 'My Baking Addiction':
			_xpath = "//*[@id='content']/div[1]/div[3]/div[4]/span/p/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)

		elif recipe['publisher'] == 'Simply Recipes':
			_xpath = "//*[@id='post-10516']/div[1]/div[6]/div[5]/div/p/text()"
			filtered_html = tree.xpath(_xpath)
			filtered_html = "\n".join(filtered_html)


		# print '*******'
		# print recipe['title']
		# print filtered_html
		# if filtered_html[0] == '[':
		
		recipe_id = recipe['recipe_id']
		param_dict = {'key': api_key, 'rId':recipe_id}
		response = requests.get('http://food2fork.com/api/get', params=param_dict)

		new_recipe, created = Recipe.objects.get_or_create(name=recipe['title'])
		new_recipe.name = recipe['title']
		new_recipe.slug = slugify(recipe['title'])
		try:
			new_recipe.steps = filtered_html
		except:
			pass
		
		new_recipe.website = recipe['source_url']

		image = urllib.urlretrieve(recipe['image_url'])
		new_recipe.image.save(os.path.basename(recipe['image_url']), File(open(image[0])))
	    
		response = response.json()
		ingredients = response['recipe']['ingredients']
		for ingredient in ingredients:
			new_ingredient, created = Ingredient.objects.get_or_create(name=ingredient)

	       
			new_recipe.ingredients.add(new_ingredient)
	        try:
	        	new_ingredient.save()
	        except:
	        	print "oops try again"
	   
		try:
			new_recipe.save()   
		except:
			print "oops try again"
		

		# image = urllib.urlretrieve(recipe['image_url'])
		# recipe_id = recipe['recipe_id']
		# param_dict = {'key': api_key, 'rId':recipe_id}
		# response = requests.get('http://food2fork.com/api/get', params=param_dict)
		# response = response.json()
		# # print response['recipe']['ingredients']

		# new_recipe, created = Recipe.objects.get_or_create(name = recipe['title'])
		# new_recipe.ingredients = response['recipe']['ingredients']
		# new_recipe.image.save(os.path.basename(recipe['image_url']), File(open(image[0])))

