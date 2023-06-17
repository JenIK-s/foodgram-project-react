from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters

from recipes.models import (
    FavoritesList,
    Ingredient,
    Recipe,
    ShoppingList,
    Tag
)
from .filters import RecipeFilter, IngredientFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeAddSerializer,
    RecipeSerializer,
    SubscriptionSerializer,
    SubscribeRecipeSerializer,
    TagSerializer
)
from users.models import User, Subscription


class UserViewSet(UserViewSet):
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                Subscription.objects.create(user=request.user, author=author),
                context={'request': request},
            )
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        Subscription.objects.filter(user=request.user, author=author).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            image=self.request.data.get('image')
        )

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

            return Response(serializer.data, status=HTTP_201_CREATED)

        cart = model.objects.filter(user=request.user, recipe__id=id)
        if not cart.exists():
            return Response(
                {
                    'error': 'Рецепт уже удалён из корзины.'
                },
                status=HTTP_400_BAD_REQUEST
            )
        cart.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.operations_shopping_and_favorite_cart(
            request,
            pk,
            FavoritesList
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.operations_shopping_and_favorite_cart(
            request,
            pk,
            ShoppingList
        )

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        purchases = ShoppingList.objects.filter(user=request.user)
        settings.FILE_NAME = 'shopping-list.txt'
        with open(settings.FILE_NAME, 'w') as f:
            for elem in purchases:
                recipe = elem.recipe
                result_str = str(
                    f'Автор рецепта: {recipe.author}\n'
                    + f'Название рецепта: {recipe.name}\n'
                    + f'Описание: {recipe.text}\n'
                )
                f.write(result_str + '\n')

        return FileResponse(open(settings.FILE_NAME, 'rb'), as_attachment=True)
