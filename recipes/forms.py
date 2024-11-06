from django import forms
from .models import Recipe,Collection,Ingredient,Image
from django.forms import inlineformset_factory


class CollectionCreateForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    title=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Collection Title'}),
        required=True
    )
    
    class Meta:
        model = Collection
        fields = ['title', 'recipes']
        
        
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'author', 'cuisine', 'food_type', 'difficulty_level',
            'instructions', 'servings', 'preparation_time', 'total_time',
            'calories', 'featured'
        ]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit', 'is_optional']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    fields=['name', 'quantity', 'unit', 'is_optional'], extra=1, can_delete=True
)

ImageFormSet = inlineformset_factory(
    Recipe, Image, form=ImageForm,
    fields=['image'], extra=1, can_delete=True
)