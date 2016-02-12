from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from main.slug import unique_slugify

class Ingredient(models.Model):
	name = models.CharField(max_length=255)
	

	def __unicode__(self):
		return self.name 

	def get_absolute_url(self):
		return reverse('main.views.success')

class Recipe(models.Model):
	name = models.CharField(max_length=255)
	ingredients = models.ManyToManyField(Ingredient)
	steps = models.TextField()
	slug = models.SlugField(max_length=255, unique=True, help_text='A label for URL config.')
	website = models.URLField(blank=True)
	image = models.ImageField(upload_to='media')

	def __unicode__(self):
		return self.name 

	def get_absolute_url(self):
		return reverse('main.views.listview')

	def save(self, **kwargs):
		slug = '%s' % (self.name)
		unique_slugify(self, slug)
		super(Recipe, self).save()
