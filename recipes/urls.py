from django.urls import path
from . import views


app_name='recipe'
urlpatterns=[
    path('',views.home_page,name='home_page'),
    path('recipes/',views.RecipeListView.as_view(),name='recipe_list'),
    path('recipe/<int:pk>/',views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('collections/',views.CollectionListView.as_view(),name='collection_list'),
    path('collection/<int:pk>/',views.CollectionDetailView.as_view(),name='collection_detail'),
    path('collection/create/',views.CollectionCreateView.as_view(),name='collection_create'),
    path('collection/<int:pk>/edit/',views.CollectionUpdateView.as_view(),name='collection_edit'),
    path('collection/<int:pk>/delete/',views.CollectionDeleteView.as_view(),name='collection_delete'),
    path('recipe/create/',views.create_recipe,name='recipe_create'),
    path('recipe/<int:pk>/edit/',views.update_recipe,name='recipe_edit'),
    path('recipe/<int:pk>/delete/',views.RecipeDeleteView.as_view(),name='recipe_delete'),
]