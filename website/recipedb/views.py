from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse

from .models import Recipe

def home(request):
    return render(request, 'recipedb/home.html')

def recipe_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipedb/recipe_page.html', {'recipe': recipe})
