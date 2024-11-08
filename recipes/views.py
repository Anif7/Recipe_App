from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Collection,Recipe,Ingredient
from django.core.paginator import Paginator
from django.urls import reverse_lazy,reverse
from .forms import CollectionCreateForm,RecipeForm,IngredientFormSet,ImageFormSet
from django.contrib import messages
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .filters import RecipeFilter,CollectionFilter

def home_page(request):
    return render(request,'home.html')
    

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6
    filterset_class = RecipeFilter  

    def get_queryset(self):
        queryset = Recipe.objects.all()
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'calories_low_high':
            queryset = queryset.order_by('calories')
        elif sort_by == 'calories_high_low':
            queryset = queryset.order_by('-calories')
        elif sort_by == 'created_at_new_old':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'created_at_old_new':
            queryset = queryset.order_by('created_at')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort_by')
        featured_recipes = Recipe.objects.filter(featured=True)
        if sort_by == 'calories_low_high':
            featured_recipes = featured_recipes.order_by('calories')
        elif sort_by == 'calories_high_low':
            featured_recipes = featured_recipes.order_by('-calories')
        elif sort_by == 'created_at_new_old':
            featured_recipes = featured_recipes.order_by('-created_at')
        elif sort_by == 'created_at_old_new':
            featured_recipes = featured_recipes.order_by('created_at')
        self.filterset_featured = self.filterset_class(self.request.GET, queryset=featured_recipes)
        context['featured_recipes_page'] = self.filterset_featured.qs

        paginator = Paginator(context['featured_recipes_page'], 6)
        page_number = self.request.GET.get('featured_page')
        context['featured_recipes_page'] = paginator.get_page(page_number)

        context['filter'] = self.filterset
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
    
    def get_queryset(self):
        queryset=Collection.objects.all()
        self.filterset=CollectionFilter(self.request.GET,queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['total_collections']=Collection.objects.all().count()
        context['filter']=self.filterset
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
    
    
class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, instance=self.object, prefix='ingredients')
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='images')
        else:
            context['ingredient_formset'] = IngredientFormSet(prefix='ingredients')
            context['image_formset'] = ImageFormSet(prefix='images')
        return context

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()

        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        image_formset = context['image_formset']
        
        if ingredient_formset.is_valid() and image_formset.is_valid():
            ingredient_formset.instance = recipe
            image_formset.instance = recipe
            ingredient_formset.save()
            image_formset.save()
            
            messages.success(self.request, "Recipe successfully created.")
            return redirect(self.get_success_url(recipe))
        else:
            return self.form_invalid(form)

    def get_success_url(self,recipe):
        return reverse_lazy('recipe:recipe_detail', kwargs={'pk': recipe.pk})
        

class UpdateRecipeView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipe:recipe_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, instance=self.object, prefix='ingredients')
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='images')
        else:
            context['ingredient_formset'] = IngredientFormSet(instance=self.object, prefix='ingredients')
            context['image_formset'] = ImageFormSet(instance=self.object, prefix='images')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        image_formset = context['image_formset']
        
        if form.is_valid() and ingredient_formset.is_valid() and image_formset.is_valid():
            response = super().form_valid(form)
            ingredient_formset.save()
            image_formset.save()
            return response
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('recipe:recipe_detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(DeleteView,LoginRequiredMixin):
    model=Recipe
    template_name='recipes/recipe_delete_confirm.html'
    context_object_name='recipe'
    success_url=reverse_lazy('recipe:recipe_list')