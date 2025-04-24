from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import RecipeForm, SignUpForm


# Create your views here.
from django.http import HttpResponse

from .models import Recipe

def home(request):
    return render(request, 'recipedb/home.html')

def recipe_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipedb/recipe_page.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.instance.u_id = request.user
            form.save()  # or do something else with the data
            return redirect('home')  # or wherever you want to go after
    else:
        form = RecipeForm()
    return render(request, 'recipedb/add_recipe.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after sign-up
            login(request, user)
            return redirect('home')  # Redirect to the homepage or any page you like
    else:
        form = SignUpForm()

    return render(request, 'recipedb/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a specific page after login
    else:
        form = AuthenticationForm()

    return render(request, 'recipedb/login.html', {'form': form})