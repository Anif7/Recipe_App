from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Collection,Recipe,Ingredient
from django.core.paginator import Paginator
from django.urls import reverse_lazy,reverse
from .forms import CollectionCreateForm

def home_page(request):
    return render(request,'home.html')
    

class RecipeListView(ListView):
    model=Recipe
    template_name='recipe_list.html'
    context_object_name='recipes'
    paginate_by=3
    ordering = ['-created_at']
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        featured_recipes=Recipe.objects.filter(featured=True).order_by('-created_at')
        paginator=Paginator(featured_recipes,6)
        page_number=self.request.GET.get('featured_page')
        context['featured_recipes_page']=paginator.get_page(page_number)
        return context


class RecipeDetailView(DetailView):
    model=Recipe
    template_name='recipes/recipe_detail.html'
    context_object_name='recipe'


class CollectionListView(ListView):
    model=Collection
    template_name='collection/collections_list.html'
    context_object_name='collections'
    paginate_by=6
    ordering = ['title']
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['total_collections']=Collection.objects.all().count()
        return context


class CollectionDetailView(DetailView):
    model=Collection
    template_name='collection/collection_detail.html'
    context_object_name='collection'
    
    
class CollectionCreateView(CreateView):
    model = Collection
    template_name = 'collection/collection_form.html'
    form_class = CollectionCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('recipe:collection_detail',kwargs={'pk':self.object.pk})
    
    
class CollectionUpdateView(UpdateView):
    model=Collection
    template_name='collection/collection_form.html'
    form_class=CollectionCreateForm
    context_object_name='collection'

    def get_queryset(self):
        return Collection.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('recipe:collection_detail',kwargs={'pk':self.object.pk})
    
    
class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'collection/collection_confirm_delete.html'
    context_object_name = 'collection'
    success_url = reverse_lazy('recipe:collection_list')

    def get_queryset(self):
        return Collection.objects.filter(author=self.request.user)