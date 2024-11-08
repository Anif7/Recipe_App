import django_filters
from .models import Recipe
from django.contrib.auth.models import User

class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Search by title')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Author')
    cuisine = django_filters.ChoiceFilter(choices=Recipe.CUISINE_CHOICES)
    difficulty_level = django_filters.ChoiceFilter(choices=Recipe.DIFFICULTY_CHOICES)
    food_type = django_filters.ChoiceFilter(choices=Recipe.FOOD_TYPE_CHOICE)

    class Meta:
        model = Recipe
        fields = ['title', 'author', 'cuisine', 'difficulty_level', 'food_type']

