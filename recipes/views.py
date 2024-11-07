from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Collection,Recipe,Ingredient
from django.core.paginator import Paginator
from django.urls import reverse_lazy,reverse
from .forms import CollectionCreateForm,RecipeForm,IngredientFormSet,ImageFormSet
from django.contrib import messages
from django.forms import ValidationError

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
    
    
def create_recipe(request):
    if request.method == 'POST':
        # Create a new Recipe instance since we are creating a new recipe
        recipe = Recipe()

        # Create form instances for the recipe, ingredients, and images
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        image_formset = ImageFormSet(request.POST, request.FILES, instance=recipe, prefix='images')

        # Check if all forms are valid
        if form.is_valid() and ingredient_formset.is_valid() and image_formset.is_valid():
            recipe = form.save(commit=False)  # Save the recipe instance without committing to the DB yet

            # Automatically set the author as the current logged-in user
            recipe.author = request.user

            # Save the recipe instance with the author set
            recipe.save()

            # Save ingredients and images associated with the recipe
            ingredients = ingredient_formset.save(commit=False)
            images = image_formset.save(commit=False)

            # Validate and save each ingredient
            for ingredient in ingredients:
                if ingredient.quantity is None or ingredient.quantity <= 0:
                    ingredient_formset.errors.append(ValidationError(
                        'Quantity must be a positive number.'
                    ))
                    # Return the form with errors
                    return render(request, 'recipes/recipe_form.html', {
                        'form': form,
                        'ingredient_formset': ingredient_formset,
                        'image_formset': image_formset,
                    })
                ingredient.recipe = recipe
                ingredient.save()

            # Save each image
            for image in images:
                image.recipe = recipe
                image.save()

            # Save formsets (ingredients and images)
            ingredient_formset.save()
            image_formset.save()

            # Redirect to the recipe detail page after successful creation
            messages.success(request, "Recipe successfully created.")
            return redirect('recipe:recipe_detail', pk=recipe.pk)

        else:
            # If the form is not valid, show an error message
            messages.error(request, "There was an error with your submission. Please correct it below.")

    else:
        # Initialize empty forms for creating a new recipe
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        image_formset = ImageFormSet(prefix='images')

    # Context for the template to display
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'image_formset': image_formset,
    }

    return render(request, 'recipes/recipe_form.html', context)



# def recipe_create_or_update(request, recipe_id=None):
#     if recipe_id:
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         message_action = "updated"
#     else:
#         recipe = Recipe()
#         message_action = "created"
#     if request.method == "POST":
#         form = RecipeForm(request.POST, request.FILES, instance=recipe)
#         ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix="ingredients")
#         image_formset = ImageFormSet(request.POST, request.FILES, instance=recipe, prefix="images")
#         if form.is_valid() and ingredient_formset.is_valid() and image_formset.is_valid():
#             recipe.author = request.user
#             recipe = form.save()
#             ingredient_formset.instance = recipe
#             image_formset.instance = recipe
#             ingredient_formset.save()
#             image_formset.save()
#             messages.success(request, f"Recipe successfully {message_action}.")
#             return redirect("recipe:recipe_detail", pk=recipe.id)
#         else:
#             messages.error(request, "There was an error with your submission. Please correct it below.")
#     else:
#         form = RecipeForm(instance=recipe)
#         ingredient_formset = IngredientFormSet(instance=recipe, prefix="ingredients")
#         image_formset = ImageFormSet(instance=recipe, prefix="images")
#     context = {
#         "form": form,
#         "ingredient_formset": ingredient_formset,
#         "image_formset": image_formset,
#         "recipe": recipe,
#         "initial_ingredients": ingredient_formset.initial,  
#         "initial_images": image_formset.initial, 
#     }
#     return render(request, "recipes/recipe_form.html", context)


# def update_recipe(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, instance=recipe)
#         ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
#         image_formset = ImageFormSet(request.POST, request.FILES, instance=recipe, prefix='images')

#         if form.is_valid() and ingredient_formset.is_valid() and image_formset.is_valid():
#             recipe = form.save()
#             # Save formsets, including handling deletions
#             ingredient_formset.save()  # This will delete marked ingredients
#             image_formset.save()  # This will delete marked images
#             return redirect('recipe:recipe_detail', pk=recipe.pk)
#     else:
#         form = RecipeForm(instance=recipe)
#         ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
#         image_formset = ImageFormSet(instance=recipe, prefix='images')

#     return render(request, 'recipes/recipe_form.html', {
#         'form': form,
#         'ingredient_formset': ingredient_formset,
#         'image_formset': image_formset,
#     })


def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        image_formset = ImageFormSet(request.POST, request.FILES, instance=recipe, prefix='images')
        
        if form.is_valid() and ingredient_formset.is_valid() and image_formset.is_valid():
            recipe = form.save()
            ingredient_formset.save()
            image_formset.save()
            return redirect('recipe:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        image_formset = ImageFormSet(instance=recipe, prefix='images')

    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'image_formset': image_formset,
    })



