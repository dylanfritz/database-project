from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, RecipeIngredient

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

# TODO
# ingredients
# shopping list
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