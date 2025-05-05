from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import UserProfile, Ingredient, Recipe, ShoppingList, ShoppingListItem, RecipeList
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from .forms import RecipeForm, SignUpForm, RecipeIngredientFormSet, ShoppingListItemForm, AddIngredientForm
from django.http import JsonResponse
import json


# Create your views here.
from django.http import HttpResponse
from .models import Recipe

@login_required(login_url='login')
def home(request):
    return render(request, 'recipedb/home.html')

@login_required
def profile(request):
    profile = request.user.userprofile
    return render(request, 'recipedb/profile.html', {'profile': profile})

# for viewing list of ingredients in database
def ingredient_page(request):
    query = request.GET.get('q', '')
    ingredients = Ingredient.objects.all()

    if query:
        ingredients = ingredients.filter(name__icontains=query)

    restricted = set()
    restricted_ingredients = set()

    # Request restricted ingredients for logged-in user
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            restricted = profile.restricted_ingredients.all().values_list('name', flat=True)
            restricted_ingredients = set(restricted)
        except UserProfile.DoesNotExist:
            pass

    ingredient_status = {ingredient.name: (ingredient.name in restricted_ingredients) for ingredient in ingredients}
    
    context = {
        'ingredients': ingredients,
        'restricted_ingredients': restricted_ingredients,
        'ingredient_status': ingredient_status,
        'query': query,  # so the form can preserve the input
    }

    return render(request, "recipedb/ingredient_page.html", context)

# for adding ingredients
def add_ingredient(request):
    if request.method == 'POST':
        form = AddIngredientForm(request.POST)
        if form.is_valid():
            ingredient= form.save()  # Save the new ingredient to the database
            substitutes = form.cleaned_data['substitutes']
            ingredient.substitutes.set(substitutes)  # Link the selected substitutes
            
            return redirect('ingredient_page')  # Redirect to the ingredient list or another page
    else:
        form = AddIngredientForm()  # Empty form for GET request
    
    return render(request, 'recipedb/add_ingredient.html', {'form': form})

# user shopping list
@login_required
def shopping_list_page(request):
    shopping_list, _ = ShoppingList.objects.get_or_create(u_id=request.user)

    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST)
        if form.is_valid():
            ingredient = form.cleaned_data['ingredient']
            quantity = form.cleaned_data['quantity']
            unit = form.cleaned_data['unit']

            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )
            return redirect('shopping_list')
    else:
        form = ShoppingListItemForm()

    items = ShoppingListItem.objects.filter(shopping_list=shopping_list)

    return render(request, 'recipedb/shopping_list.html', {
        'form': form,
        'items': items,
    })

# add ingredients to shopping list
@login_required
def add_ingredient_to_shopping_list(request, ingredient_id):
    if request.user.is_authenticated:
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
        shopping_list.ingredients.add(ingredient)
    return redirect('ingredient_page')

# remove ingredient from shopping list
@login_required
def remove_from_shopping_list(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id)
    # Make sure user owns the shopping list
    if item.shopping_list.u_id != request.user:
        return redirect('home')
    
    item.delete()
    return redirect('shopping_list') 

# handle restricted ingredient toggling
@require_POST
@login_required
def toggle_restricted_ingredient(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ingredient_name = data.get("ingredient_name")
            ingredient = Ingredient.objects.get(name=ingredient_name)
            profile = UserProfile.objects.get(user=request.user)

            if ingredient in profile.restricted_ingredients.all():
                profile.restricted_ingredients.remove(ingredient)
                status = "unrestricted"
            else:
                profile.restricted_ingredients.add(ingredient)
                status = "restricted"

            return JsonResponse({"status": status})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# for viewing a specific recipe
def recipe_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    is_owner_or_admin = request.user.is_staff or recipe.u_id == request.user
    return render(request, 'recipedb/recipe_page.html', {
        'recipe': recipe,
        'is_owner_or_admin': is_owner_or_admin,
    })

# for viewing a list of all recipes
def recipe_view(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipedb/recipe_view.html', {'recipes': recipes})

# view preferred recipes
def recipe_list_view(request):
    profile = request.user.userprofile
    favorites = profile.preferred_recipes.all()
    return render(request, 'favorite_recipes.html', {'favorites': favorites})

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
            return redirect('home')
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()
    
    return render(request, 'recipedb/add_recipe.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def edit_recipe(request, id):
    # Get the recipe by ID or return 404 if not found
    recipe = get_object_or_404(Recipe, id=id)

    # If the request is POST, it means the user is submitting the form to update the recipe
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)  # Pre-fill the form with the existing recipe data
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)  # Pre-fill the formset with ingredients

        if form.is_valid() and formset.is_valid():
            form.save()  # Save the updated recipe
            formset.save()  # Save the updated ingredients
            return redirect('recipe_page', id=recipe.id)  # Redirect to the recipe's page after saving
    else:
        # If GET request, just load the form with current recipe data
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)

    return render(request, 'recipedb/edit_recipe.html', {
        'form': form,
        'formset': formset,
        'recipe': recipe,
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
            user = form.save(commit=False)  # Don’t save to DB yet
            password = form.cleaned_data['password']
            user.set_password(password)  # Hash the password
            user.save()  # Now save the user with hashed password
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
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