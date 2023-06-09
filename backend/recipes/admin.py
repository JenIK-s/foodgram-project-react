from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
    )
    list_filter = ('author', 'title', 'tags',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'units_of_measurement',
    )
    search_fields = ('title',)
    list_filter = ('units_of_measurement',)


admin.site.register(Tag)