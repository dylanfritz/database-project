from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:id>/', views.recipe_page, name='recipe_page'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Django's built-in login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Django's built-in logout view
]
