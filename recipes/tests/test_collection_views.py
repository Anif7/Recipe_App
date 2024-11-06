from django.test import TestCase
from .test_models import InitialSetup
from django.urls import reverse,resolve
from ..views import CollectionListView,CollectionDetailView,CollectionCreateView,CollectionUpdateView,CollectionDeleteView
from ..models import Collection

class CollectionListViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.collection_list_url=reverse("recipe:collection_list")
        self.response=self.client.get(self.collection_list_url)
        
    def test_collection_list_success_code(self):
        self.assertEqual(self.response.status_code,200)
        
    def test_collection_list_url_resolves_list_view(self):
        view=resolve('/collections/')
        self.assertEqual(view.func.view_class,CollectionListView)
        
    def test_collection_list_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'collection/collections_list.html')
        
    def test_collection_list_contains_navigation_links(self):
        detail_url=reverse('recipe:collection_detail',kwargs={'pk':1})
        create_collection_url=reverse('recipe:collection_create')
        self.assertContains(self.response,'href="{0}"'.format(detail_url))
        self.assertContains(self.response,'href="{0}"'.format(create_collection_url))
        

class CollectionDetailViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.collection_detail_url=reverse('recipe:collection_detail',kwargs={'pk':1})
        self.response=self.client.get(self.collection_detail_url)
        
    def test_collection_detail_success_url(self):
        self.assertEqual(self.response.status_code,200)
        
    def test_collection_detail_url_resolves_detail_view(self):
        view=resolve('/collection/1/')
        self.assertEqual(view.func.view_class,CollectionDetailView)
        
    def test_collection_detal_view_not_found_status_code(self):
        collection_detail_url=reverse('recipe:recipe_detail',kwargs={'pk':50})
        response=self.client.get(collection_detail_url)
        self.assertEqual(response.status_code,404)
        
    def test_collection_detail_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'collection/collection_detail.html')
        
        
class CollectionCreateViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.collection_create_url=reverse('recipe:collection_create')
        self.response=self.client.get(self.collection_create_url)
        
    def test_collection_create_view_success_url(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_collection_create_view_url_resolves_correct_view(self):
        view=resolve('/collection/create/')
        self.assertEqual(view.func.view_class,CollectionCreateView)
        
        
class CollectionUpdateViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.collection_update_url=reverse('recipe:collection_edit',kwargs={'pk':self.collection.pk})
        self.client.login(username='anif', password='anif123')
        self.response=self.client.get(self.collection_update_url)
        
    def test_collection_update_success_code(self):
        self.assertEqual(self.response.status_code,200)
        
    def test_collection_update_view_url_resolves_correct_view(self):
        view = resolve(self.collection_update_url)
        self.assertEqual(view.func.view_class, CollectionUpdateView)
        
        
class CollectionDeleteViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.collection_update_url=reverse('recipe:collection_delete',kwargs={'pk':self.collection.pk})
        self.client.login(username='anif', password='anif123')
        self.response=self.client.get(self.collection_update_url)
        
    def test_collection_delete_success_code(self):
        self.assertEqual(self.response.status_code,200)
        
    def test_collection_delete_view_url_resolves_correct_view(self):
        view = resolve(self.collection_update_url)
        self.assertEqual(view.func.view_class, CollectionDeleteView)
        
    def test_collection_delete_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'collection/collection_confirm_delete.html')
    
    def test_collection_delete_contains_navigation_links(self):
        collection_detail_url=reverse('recipe:collection_detail',kwargs={'pk':1})
        self.assertContains(self.response,'href="{0}"'.format(collection_detail_url))
        