from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import UserProfile, Ingredient
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from .forms import RecipeForm, SignUpForm, RecipeIngredientFormSet
from django.http import JsonResponse


# Create your views here.
from django.http import HttpResponse
from .models import Recipe

def home(request):
    return render(request, 'recipedb/home.html')

@login_required
def profile(request):
    profile = request.user.userprofile
    return render(request, 'recipedb/profile.html', {'profile': profile})

# for viewing list of ingredients in database
def ingredient_page(request):
    query = request.GET.get('q')
    if query:
        ingredients = Ingredient.objects.filter(name__icontains=query)
    else:
        ingredients = Ingredient.objects.all()
    return render(request, 'recipedb/ingredient_page.html', {
        'ingredients': ingredients,
        'query': query
    })

# for viewing a specific recipe
def recipe_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipedb/recipe_page.html', {'recipe': recipe})

# for viewing a list of all recipes
def recipe_view(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipedb/recipe_view.html', {'recipes': recipes})

# for creating a new recipe
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.u_id = request.user
            recipe.save()
            formset.instance = recipe
            formset.save()
            return redirect('home')  # or wherever
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()
    
    return render(request, 'recipedb/add_recipe.html', {
        'form': form,
        'formset': formset,
    })

# handle adding a recipe to user's preferences
@require_POST
@login_required
def toggle_preference(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    if recipe in user.userprofile.preferred_recipes.all():
        user.userprofile.preferred_recipes.remove(recipe)
        status = 'removed'
    else:
        user.userprofile.preferred_recipes.add(recipe)
        status = 'added'
    return JsonResponse({'status': status})

# for creating new account
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create UserProfile
            UserProfile.objects.create(user=user)
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