from django_filters import rest_framework as filters

from recipes.models import Recipe


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
