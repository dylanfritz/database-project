from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:id>/', views.recipe_page, name='recipe_page'),
]
