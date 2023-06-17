from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'in_favorite', 'is_in_shopping_cart')

    def filter_is_favorite_or_in_shopping_cart(
            self,
            queryset,
            _,
            value,
            field_name
    ):
        if value:
            filter_parameters = {
                f"{field_name}__user": self.request.user
            }
            return queryset.filter(**filter_parameters)
        return queryset

    def filter_is_favorited(self, queryset, _, value):
        return self.filter_is_favorite_or_in_shopping_cart(
            queryset,
            _,
            value,
            field_name='in_favorite'
        )

    def filter_is_in_shopping_cart(self, queryset, _, value):
        return self.filter_is_favorite_or_in_shopping_cart(
            queryset,
            _,
            value,
            field_name='shopping_cart'
        )


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
