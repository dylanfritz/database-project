from django.db import models
from django.contrib.auth.models import User # django built-in user model, no need for custom user model

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

# UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # links to django User model 
    preferred_recipes = models.ManyToManyField('Recipe', blank=True, related_name='liked_by')
    restricted_ingredients = models.ManyToManyField('Ingredient', blank=True, related_name='restricted_by')
    
    def __str__(self):
        return f"Profile of {self.user.username}"

# Ingredient entity
class Ingredient(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    calories = models.PositiveIntegerField()

    # Ingredient-Ingredient SUBSTITUTES relationship
    # symmetrical; if x subs y then y subs x
    substitutes = models.ManyToManyField('self', symmetrical = True, blank = True)

    def __str__(self):
        return self.name

# Recipe Entity
class Recipe(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    instructions = models.TextField()

    # Recipe-Ingredient relationship
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.name

# Recipe-Ingredient CALLS_FOR relationship model
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients')

    quantity = models.DecimalField(max_digits=5, decimal_places=2) # max 999.99
    unit = models.CharField(max_length=20) # e.g., 'tsp', 'cups', 'grams'

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.name}"

# User and Ingredient STOCKS relationship
class Stocks(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=5, decimal_places=2) # max 999.99
    unit = models.CharField(max_length=20) # e.g., 'tsp', 'cups', 'grams'

# TODO
# Make models for:
# List entity
class List(models.Model):
    name = models.CharField(max_length=100)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# Recipe List entity (list subclass)
#   - lists Recipes, set and edited by User
class RecipeList(List):
    recipes = models.ManyToManyField('Recipe', related_name='in_recipe_lists')

# Shopping List entity (list subclass)
#   - lists Ingredients, set and edited by User
class ShoppingList(List):
    ingredients = models.ManyToManyField(
        Ingredient, through='ShoppingListItem', related_name='in_shopping_lists'
    )

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=20)
    
# User Restrictions (Ingredient), M:N relationship
# User.add_to_class('restricted_ingredients', models.ManyToManyField(Ingredient, related_name='restricted_by'))


###
# After making a model, don't forget to
#   register models in admin.py !
#   run python3 manage.py makemigrations
#       python3 manage.py migrate
###