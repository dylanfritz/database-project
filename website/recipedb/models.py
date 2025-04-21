from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Ingredient(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    calories = models.PositiveIntegerField()
    substitutes = models.ManyToManyField('self', symmetrical = True, blank = True)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    recipe_id = models.PositiveIntegerField(primary_key=True)
    prep_time = models.TimeField()
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    instructions = models.TextField()

    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=5, decimal_places=2) # max 999.99
    unit = models.CharField(max_length=20) # e.g., 'tsp', 'cups', 'grams'

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.name}"