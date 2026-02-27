from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('edit-recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
