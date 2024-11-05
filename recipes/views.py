from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Collection,Recipe,Ingredient
from django.core.paginator import Paginator

def home_page(request):
    return render(request,'home.html')
    

class RecipeListView(ListView):
    model=Recipe
    template_name='recipe_list.html'
    context_object_name='recipes'
    paginate_by=3
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        featured_recipes=Recipe.objects.filter(featured=True)
        paginator=Paginator(featured_recipes,6)
        page_number=self.request.GET.get('featured_page')
        context['featured_recipes_page']=paginator.get_page(page_number)
        return context


class RecipeDetailView(DetailView):
    model=Recipe
    template_name='recipes/recipe_detail.html'
    context_object_name='recipe'

