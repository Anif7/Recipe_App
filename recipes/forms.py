from django import forms
from .models import Recipe,Collection


class CollectionCreateForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    title=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Collection Title'}),
        required=True
    )

    class Meta:
        model = Collection
        fields = ['title', 'recipes']