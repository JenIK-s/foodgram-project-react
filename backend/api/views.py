from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (FavoritesList, Ingredient, IngredientInRecipe, Recipe,
                          ShoppingList, Tag)
from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer,
                          RecipeAddSerializer, RecipeSerializer,
                          SubscribeRecipeSerializer,
                          TagSerializer)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeAddSerializer

    def operations_shopping_and_favorite_cart(self, request, id, model):
        if request.method == 'POST':
            if model.objects.filter(user=request.user, recipe__id=id):
                return Response(
                    {
                        'error': 'Рецепт уже находится в корзине.'
                    }
                )
            recipe = get_object_or_404(Recipe, id=id)
            model.objects.create(user=request.user, recipe=recipe)
            serializer = SubscribeRecipeSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            cart = model.objects.filter(user=request.user, recipe__id=id)
            if not cart.exists():
                return Response(
                    {
                        'error': 'Рецепт уже удалён из корзины.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
   
    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.operations_shopping_and_favorite_cart(request, pk, FavoritesList)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.operations_shopping_and_favorite_cart(request, pk, ShoppingList)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        purchases = ShoppingList.objects.filter(user=user)
        file = 'shopping-list.txt'
        print(purchases)
        # with open(file, 'w', encoding='utf-8') as f:
        #     shop_cart = dict()
        #     for purchase in purchases:
        #         ingredients = IngredientInRecipe.objects.filter(
        #             recipe=purchase.recipe.id
        #         )
        #         for r in ingredients:
        #             i = Ingredient.objects.get(pk=r.ingredient.id)
        #             point_name = f'{i.name} ({i.measurement_unit})'
        #             if point_name in shop_cart.keys():
        #                 shop_cart[point_name] += r.amount
        #             else:
        #                 shop_cart[point_name] = r.amount

        #     for name, amount in shop_cart.items():
        #         f.write(f'* {name} - {amount}\n')

        # return FileResponse(open(file, 'rb'), as_attachment=True)