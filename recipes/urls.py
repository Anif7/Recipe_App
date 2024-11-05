from django.urls import path
from . import views


app_name='recipe'
urlpatterns=[
    path('',views.home_page,name='home_page'),
    path('recipes/',views.RecipeListView.as_view(),name='recipe_list'),
    path('recipe/<int:pk>/',views.RecipeDetailView.as_view(), name='recipe_detail'),
]