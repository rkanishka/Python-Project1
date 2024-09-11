from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe

def home(request):
    return render(request, 'recipes/home.html')

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 10

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'