from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
from ..models import Recipe, Ingredient, Image
from django.contrib.auth import get_user_model
from PIL import Image as PILImage
import io

def get_temporary_image():
    """Create a valid temporary image file."""
    image = PILImage.new('RGB', (100, 100)) 
    temp_image = io.BytesIO()
    image.save(temp_image, format='JPEG') 
    temp_image.seek(0)
    return SimpleUploadedFile('temp_image.jpg', temp_image.read(), content_type='image/jpeg')


class CreateRecipeFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='anif', password='anif123')
        self.client.login(username='anif', password='anif123')
        self.create_recipe_url = reverse('recipe:recipe_create')  
    
    def test_get_create_recipe_view(self):
        """Test GET request for recipe creation form."""
        response = self.client.get(self.create_recipe_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
    
    def test_post_valid_recipe_data(self):
        """Test valid POST request to create a recipe with ingredients and images."""
        image_data = SimpleUploadedFile("home-img-1.jpg", b"file_content", content_type="image/jpeg")

        data = {
            'title': 'Test Recipe',
            'cuisine': 'indian',
            'food_type': 'veg',
            'difficulty_level': 'easy',
            'instructions': 'Instructions',
            'servings': 6,
            'preparation_time': '00:20:00',
            'total_time': '00:20:00',
            'calories': 250,
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-name': 'Salt',
            'ingredients-0-quantity': '1',
            'ingredients-0-unit': 'gms',
            'ingredients-1-name': 'Pepper',
            'ingredients-1-quantity': '2',
            'ingredients-1-unit': 'gms',
            'images-TOTAL_FORMS': '1',
            'images-INITIAL_FORMS': '0',
        }

        files = {
            'images-0-image': image_data,
        }

        response = self.client.post(reverse('recipe:recipe_create'), data=data, files=files, follow=True)
        recipe = Recipe.objects.get(title='Test Recipe')
        self.assertRedirects(response, reverse('recipe:recipe_detail', kwargs={'pk': recipe.pk}))
        self.assertTrue(Recipe.objects.filter(title='Test Recipe').exists())
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_post_invalid_recipe_data(self):
        """Test POST request with invalid recipe data."""
        image_data = SimpleUploadedFile("home-img-1.jpg", b"file_content", content_type="image/jpeg")

        data = {
            'title': '',
            'cuisine': 'indian',
            'food_type': 'veg',
            'difficulty_level': 'easy',
            'instructions': 'Instructions',
            'servings': 6,
            'preparation_time': '00:20:00',
            'total_time': '00:20:00',
            'calories': 250,
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-name': 'Salt',
            'ingredients-0-quantity': '1',
            'ingredients-0-unit': 'gms',
            'ingredients-1-name': 'Pepper',
            'ingredients-1-quantity': '2',
            'ingredients-1-unit': 'gms',
            'images-TOTAL_FORMS': '1',
            'images-INITIAL_FORMS': '0',
        }

        files = {
            'images-0-image': image_data,
        }

        response = self.client.post(reverse('recipe:recipe_create'), data=data, files=files, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipe.objects.exists())
    
    def test_ingredient_quantity_validation(self):
        """Test validation for ingredient quantity."""
        image_data = SimpleUploadedFile("home-img-1.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'title': 'Test Recipe',
            'cuisine': 'indian',
            'food_type': 'veg',
            'difficulty_level': 'easy',
            'instructions': 'Mix ingredients and cook.',
            'servings': 2,
            'preparation_time': '00:10:00',
            'total_time': '00:20:00',
            'calories': 100,
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-name': 'Salt',
            'ingredients-0-quantity': '-1',
            'ingredients-0-unit': 'gms',
            'images-TOTAL_FORMS': '1',
            'images-INITIAL_FORMS': '0',
        }
        files = {
            'images-0-image': image_data,
        }
        response = self.client.post(reverse('recipe:recipe_create'), data=data, files=files, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ingredient.objects.exists())


class UpdateRecipeFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')

        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            cuisine='indian',
            food_type='veg',
            difficulty_level='easy',
            instructions='Test instructions',
            servings=4,
            preparation_time= timedelta(minutes=20),
            total_time= timedelta(minutes=30),
            calories=200,
            author=self.user
        )
        Ingredient.objects.create(
            name='Tomato',
            quantity=2,
            unit='gms',
            recipe=self.recipe
        )
        Image.objects.create(
            image=get_temporary_image(),
            recipe=self.recipe
        )

    def test_update_recipe_form_valid_data(self):
        self.client.login(username='testuser', password='password')

        updated_data = {
            'title': 'Updated Recipe Title',
            'cuisine': 'indian',
            'food_type': 'veg',
            'difficulty_level': 'easy',
            'instructions': 'Updated instructions',
            'servings': 6,
            'preparation_time': '00:20:00',
            'total_time': '00:20:00',
            'calories': 250,
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '1',
            'ingredients-0-id': 1, 
            'ingredients-0-name': 'Salt',
            'ingredients-0-quantity': '1',
            'ingredients-0-unit': 'gms',
            'ingredients-1-name': 'Pepper',
            'ingredients-1-quantity': '2',
            'ingredients-1-unit': 'gms',
            'images-TOTAL_FORMS': '1',
            'images-INITIAL_FORMS': '0',
            'images-0-image': get_temporary_image(),
                }

        response = self.client.post(
            reverse('recipe:recipe_edit', kwargs={'pk': self.recipe.pk}),
            updated_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Updated Recipe Title') 
        updated_recipe = Recipe.objects.get(pk=self.recipe.pk)
        self.assertEqual(updated_recipe.title, 'Updated Recipe Title')
        self.assertEqual(updated_recipe.calories, 250)

    def test_update_recipe_form_invalid_data(self):
        self.client.login(username='testuser', password='password')

        invalid_data = {
            'title': '',
            'cuisine': 'indian', 
            'food_type': 'veg',
            'difficulty_level': 'easy', 
            'instructions': 'Updated instructions',
            'servings': 6,
            'preparation_time': timedelta(minutes=20),
            'total_time': timedelta(minutes=20),
            'calories': 250,
        }

        response = self.client.post(reverse('recipe:recipe_edit', kwargs={'pk': self.recipe.pk}), invalid_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)  
        self.assertIn('title', form.errors) 
        self.assertIn('This field is required.', form.errors['title']) 
        updated_recipe = Recipe.objects.get(pk=self.recipe.pk)
        self.assertEqual(updated_recipe.title, 'Test Recipe') 


