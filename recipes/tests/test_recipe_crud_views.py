from django.urls import reverse, resolve
from ..views import create_recipe, update_recipe, RecipeDeleteView
from .test_models import InitialSetup


class RecipeCreateViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.recipe_create_url = reverse('recipe:recipe_create')
        self.client.login(username='anif', password='anif123')
        self.response = self.client.get(self.recipe_create_url)

    def test_recipe_create_view_success_url(self):
        self.assertEqual(self.response.status_code, 200)

    def test_recipe_create_view_url_resolves_correct_view(self):
        view = resolve('/recipe/create/')
        self.assertEqual(view.func, create_recipe)

    def test_recipe_create_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/recipe_form.html')


class RecipeUpdateViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.recipe_update_url = reverse('recipe:recipe_edit', kwargs={'pk': self.recipe.pk})
        self.client.login(username='anif', password='anif123')
        self.response = self.client.get(self.recipe_update_url)

    def test_recipe_update_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_recipe_update_view_url_resolves_correct_view(self):
        view = resolve(self.recipe_update_url)
        self.assertEqual(view.func, update_recipe)

    def test_recipe_update_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/recipe_form.html')


class RecipeDeleteViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.recipe_delete_url = reverse('recipe:recipe_delete', kwargs={'pk': self.recipe.pk})
        self.client.login(username='anif', password='anif123')
        self.response = self.client.get(self.recipe_delete_url)

    def test_recipe_delete_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_recipe_delete_view_url_resolves_correct_view(self):
        view = resolve(self.recipe_delete_url)
        self.assertEqual(view.func.view_class, RecipeDeleteView)

    def test_recipe_delete_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/recipe_delete_confirm.html')

    def test_recipe_delete_view_contains_navigation_links(self):
        recipe_list_url = reverse('recipe:recipe_list')
        self.assertContains(self.response, f'href="{recipe_list_url}"')





