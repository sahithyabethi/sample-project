from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Recipe, Ingredient, Favorite
from django.db.models import Q

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                if user.is_staff:
                    return redirect('admin_dashboard')
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

@login_required
def dashboard(request):
    requested_ingredients = request.GET.get('ingredients', '').strip()
    search_query = request.GET.get('search', '').strip()
    
    matched_recipes = []
    searched_recipes = []
    
    # Priority to search if search_query is present
    if search_query:
        searched_recipes = Recipe.objects.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        ).prefetch_related('ingredients').distinct()
        
    elif requested_ingredients:
        user_ings = [i.strip().lower() for i in requested_ingredients.split(',') if i.strip()]
        all_recipes = Recipe.objects.prefetch_related('ingredients').all()
        
        for recipe in all_recipes:
            recipe_ings = [i.name.lower() for i in recipe.ingredients.all()]
            matches = set(user_ings) & set(recipe_ings)
            
            if matches:
                percentage = int((len(matches) / len(recipe_ings)) * 100) if recipe_ings else 0
                matched_recipes.append({
                    'recipe': recipe,
                    'match_percentage': percentage
                })
        
        # Sort by match percentage descending
        matched_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)

    context = {
        'requested_ingredients': requested_ingredients,
        'search_query': search_query,
        'matched_recipes': matched_recipes,
        'searched_recipes': searched_recipes,
    }
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    recipes = Recipe.objects.all()
    return render(request, 'admin_dashboard.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        prep_time = request.POST.get('prep_time')
        instructions = request.POST.get('instructions')
        image = request.FILES.get('image')
        
        recipe = Recipe.objects.create(
            name=name,
            description=description,
            prep_time=prep_time,
            instructions=instructions,
            image=image
        )
        messages.success(request, "Recipe added successfully!")
        return redirect('admin_dashboard')
    
    return render(request, 'recipe_form.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        recipe.name = request.POST.get('name')
        recipe.description = request.POST.get('description')
        recipe.prep_time = request.POST.get('prep_time')
        recipe.instructions = request.POST.get('instructions')
        if request.FILES.get('image'):
            recipe.image = request.FILES.get('image')
        recipe.save()
        messages.success(request, "Recipe updated successfully!")
        return redirect('admin_dashboard')
    
    return render(request, 'recipe_form.html', {'recipe': recipe})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    messages.success(request, "Recipe deleted.")
    return redirect('admin_dashboard')
