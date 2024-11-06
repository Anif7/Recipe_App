from django import forms
from .models import Recipe,Collection


class CollectionCreateForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(queryset=Recipe.objects.all(), required=False)

    class Meta:
        model = Collection
        fields = ['title', 'recipes']