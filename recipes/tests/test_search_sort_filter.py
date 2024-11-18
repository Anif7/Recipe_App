from django.test import TestCase
from django.urls import reverse
from ..models import Recipe,Collection,Image,Ingredient
from django.contrib.auth.models import User
from datetime import timedelta
from ..filters import RecipeFilter,CollectionFilter

class InitialSetup(TestCase):
    def setUp(self):
        self.user1=User.objects.create_user(username='anif',password='anif123')
        self.user2=User.objects.create_user(username='ravi',password='ravi123')
        self.recipe1=Recipe.objects.create(
            title='dosa',
            author=self.user1,
            cuisine='indian',
            difficulty_level="easy",
            instructions="test instruction",
            food_type="veg",
            servings=2,
            preparation_time=timedelta(minutes=20),
            total_time=timedelta(minutes=30),
            calories=150,
        )
        self.recipe2=Recipe.objects.create(
            title='biryani',
            author=self.user2,
            cuisine='mexican',
            difficulty_level="moderate",
            instructions="test instruction",
            food_type="non_veg",
            servings=2,
            preparation_time=timedelta(minutes=20),
            total_time=timedelta(minutes=30),
            calories=300,
        )
        self.collection1=Collection.objects.create(title='Desserts Collection', author=self.user1)
        self.collection2=Collection.objects.create(title='Healthy Recipes Collection', author=self.user1)
        self.collection3=Collection.objects.create(title='Home made food', author=self.user2)
    

class RecipeSearchTest(InitialSetup):
    def test_search_by_title_exact_match(self):
        data={'title':'dosa'}
        filtered_recipes=RecipeFilter(data=data).qs
        self.assertEqual(filtered_recipes.count(),1)
        self.assertEqual(filtered_recipes.first().title,'dosa')
        
    def test_search_by_title_partial_match(self):
        data={'title':'do'}
        filtered_recipes = RecipeFilter(data=data).qs
        self.assertEqual(filtered_recipes.count(), 1)
        self.assertEqual(filtered_recipes.first().title,'dosa')
        
    def test_search_no_results(self):
        data = {'title': 'Nonexistent Recipe'}
        filtered_recipes = RecipeFilter(data=data).qs
        self.assertEqual(filtered_recipes.count(), 0)
        
class RecipeFilterTests(InitialSetup):
    def test_filter_by_cuisine(self):
        response=self.client.get(reverse('recipe:recipe_list'),{'cuisine':'indian'})
        self.assertContains(response,self.recipe1.title)
        self.assertNotContains(response, self.recipe2.title)
        
    def test_filter_by_difficulty(self):
         response = self.client.get(reverse('recipe:recipe_list'), {'difficulty_level': 'moderate'})
         self.assertContains(response, self.recipe2.title)
         self.assertNotContains(response, self.recipe1.title)
        
    def test_filter_by_food_type(self):
        response=self.client.get(reverse('recipe:recipe_list'),{'food_type':'veg'})
        self.assertContains(response,self.recipe1.title)
        self.assertNotContains(response,self.recipe2.title)
    
    def test_filter_by_author(self):
        response=self.client.get(reverse('recipe:recipe_list'),{'author':2})
        self.assertContains(response,self.recipe2.title)
        self.assertNotContains(response,self.recipe1.title)
        
class RecipeSortingTests(InitialSetup):
    def test_sort_by_calories_descending(self):
        response=self.client.get(reverse('recipe:recipe_list'),{'sort_by':'calories_high_low'})
        recipes=list(response.context['recipes'])
        self.assertEqual(recipes[0].calories,300)
        self.assertEqual(recipes[1].calories, 150)
        
    def test_sort_by_calories_ascending(self):
        response = self.client.get(reverse('recipe:recipe_list'), {'sort_by': 'calories_low_high'})
        recipes = list(response.context['recipes'])
        self.assertEqual(recipes[0].calories, 150)
        self.assertEqual(recipes[1].calories, 300)
         

class CollectionFilterTest(InitialSetup):
     def test_search_by_collection_title_exact_match(self):
        data = {'title': 'Desserts Collection'}
        filtered_collections = CollectionFilter(data=data).qs
        self.assertEqual(filtered_collections.count(), 1)
        self.assertEqual(filtered_collections.first().title, 'Desserts Collection')
    
     def test_search_by_collection_title_partial_match(self):
        data = {'title': 'Healthy'}
        filtered_collections = CollectionFilter(data=data).qs
        self.assertEqual(filtered_collections.count(), 1)
        self.assertEqual(filtered_collections.first().title, 'Healthy Recipes Collection')
    
     def test_search_no_results(self):
        data = {'title': 'Nonexistent Collection'}
        filtered_collections = CollectionFilter(data=data).qs
        self.assertEqual(filtered_collections.count(), 0)
        
     def test_filter_by_author(self):
         response=self.client.get(reverse('recipe:collection_list'),{'author':2})
         self.assertContains(response,self.collection3.title)
         self.assertNotContains(response,self.collection1.title)
         self.assertNotContains(response,self.collection2.title)
        
         

         
