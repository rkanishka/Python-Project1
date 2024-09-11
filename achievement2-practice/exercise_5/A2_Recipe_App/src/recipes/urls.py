from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<uuid:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
]