from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Ingredient)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.Recipe)
admin.site.register(models.List)
admin.site.register(models.RecipeList)
admin.site.register(models.ShoppingList)