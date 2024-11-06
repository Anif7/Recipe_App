from django.test import TestCase
from ..models import Collection,Recipe
from datetime import timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from .test_models import InitialSetup
from ..forms import CollectionCreateForm

class CollectionFormTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.recipe2=Recipe.objects.create(
            title='dosa',
            author=self.user,
            cuisine='indian',
            difficulty_level="easy",
            instructions="test instruction",
            servings=2,
            preparation_time=timedelta(minutes=20),
            total_time=timedelta(minutes=30),
            calories=150,
        )
        
    def test_Collection_create_form_with_valid_data(self):
        self.client.login(username='anif', password='anif123')
        data={
            'title':'new Collection',
            'recipes':[self.recipe.id,self.recipe2.id],
        }
        
        response=self.client.post(reverse('recipe:collection_create'),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('recipe:collection_detail',kwargs={'pk':2}))
        collection=Collection.objects.last()
        self.assertEqual(collection.title,'new Collection')
        self.assertEqual(collection.recipes.count(),2)
        
    def test_Collection_create_form_with_invalid_data(self):
        self.client.login(username='anif',password='anif123')
        data={
            'title':'',
            'recipes':[],
        }
        response=self.client.post(reverse("recipe:collection_create"),data)
        self.assertEqual(response.status_code,200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])
        
    def test_collection_create_view_context(self):
        self.client.login(username='anif',password='anif123')
        response=self.client.get(reverse('recipe:collection_create'))
        self.assertEqual(response.status_code,200)
        self.assertIn('form',response.content.decode('utf-8'))
        self.assertIsInstance(response.context['form'], CollectionCreateForm)
    
    def test_collection_create_with_non_existent_recipes(self):
        self.client.login(username='anif',password='anif123')
        data = {
        'title': 'Collection with Non-existent Recipe',
        'recipes': [999],
        }
        response=self.client.post(reverse('recipe:collection_create'),data)
        self.assertEqual(response.status_code,200)
        

class CollectionUpdateFormTest(InitialSetup):
    def setUp(self):
        super().setUp()
    
    def test_collection_update(self):
        self.client.login(username='anif',password='anif123')
        collection = Collection.objects.create(title="Old Collection", author=self.user)
        collection.recipes.add(self.recipe)
        
        response=self.client.get(reverse('recipe:collection_edit',kwargs={'pk':collection.pk}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'value="Old Collection"')
        
    def test_collection_update_invalid_data(self):
        self.client.login(username='anif',password='anif123')
        collection = Collection.objects.create(title="Old Collection", author=self.user)
        collection.recipes.add(self.recipe)
        
        data = {
        'title': '', 
        'recipes': [self.recipe.id],
        }
        response = self.client.post(reverse('recipe:collection_edit', kwargs={'pk': collection.pk}), data)
        self.assertEqual(response.status_code, 200)