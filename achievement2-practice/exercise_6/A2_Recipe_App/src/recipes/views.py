from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Recipe

def home(request):
    return render(request, 'recipes/recipes_home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipes:recipe_list')
        else:
            return render(request, 'recipes/login.html', {'error': 'Invalid credentials'})
    return render(request, 'recipes/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'recipes/success.html')

@login_required(login_url='recipes:login')
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required(login_url='recipes:login')
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})