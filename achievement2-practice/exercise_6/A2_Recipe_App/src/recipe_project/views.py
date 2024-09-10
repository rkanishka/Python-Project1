from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'recipes_home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('protected_page')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'success.html')

@login_required
def protected_view(request):
    return render(request, 'protected_page.html')