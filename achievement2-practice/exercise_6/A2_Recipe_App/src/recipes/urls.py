from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
]