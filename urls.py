from django.contrib import admin
from .models import Recipe, Ingredient, Favorite

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'prep_time', 'created_at')
    search_fields = ('name', 'description')
    inlines = [IngredientInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Favorite)
