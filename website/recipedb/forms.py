from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, RecipeIngredient, ShoppingList, ShoppingListItem

# recipes
class RecipeForm(forms.ModelForm):
  class Meta:
    model = Recipe
    fields = ['name', 'desc', 'instructions', 'prep_time']

# this form is for adding ingredients to a recipe
class RecipeIngredientForm(forms.ModelForm):
    # TODO
    # Add ability to make new ingredient if not in dropdown list
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'ingredient-select'})
        }

RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=1, can_delete=True
)

# TODO-
# ingredients
# ingredient form
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'calories', 'substitutes']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'ingredient-select'})
        }

class AddIngredientForm(forms.ModelForm):
    substitutes = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),  # Get all ingredients for substitution options
        required=False,  # Make this field optional
        widget=forms.CheckboxSelectMultiple(attrs={  # Use checkboxes for multiple selection
            'class': 'ingredient-select',
        })
    )
    class Meta:
        model = Ingredient
        fields = ['name', 'calories', 'substitutes']


# shopping list
# form for adding ingredients to list
class AddToShoppingListForm(forms.Form):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all())
    quantity = forms.DecimalField(max_digits=5, decimal_places=2)
    unit = forms.CharField(max_length=20)


class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['ingredient', 'quantity', 'unit']

# recipe list

# account registration
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data