from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'recipes/recipes_home.html')

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 10

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'


@login_required
def protected_view(request):
    return render(request, 'protected_page.html')