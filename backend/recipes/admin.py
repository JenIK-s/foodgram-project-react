from django.contrib import admin

from .models import Recipe, Tag, Ingredient, FavoritesList, ShoppingList, IngredientInRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'tag',
        'count_ingredient'
    )
    list_filter = ('author', 'title',)

    def count_ingredient(self, obj):
        return obj.ingredients.count()


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'color_key',
        'slug',
    )
    list_filter = ('title', 'color_key',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'units_of_measurement',
    )
    list_filter = ('title', 'units_of_measurement',)


@admin.register(FavoritesList)
class FavoritesListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_filter = ('user', 'recipe',)


@admin.register(ShoppingList)
class ShoppingListListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_filter = ('user', 'recipe',)
