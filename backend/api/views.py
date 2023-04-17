from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .permissions import IsReadOnly
from ..recipes.models import Recipe, Ingredient, Tag, FavoritesList
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    RecipeDetailSerializer,
    TagSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = (IsReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'author',
        'tags',
        'is_favorited',
        'is_in_shopping_list'
    ]
    search_fields = ['name', 'tags__name']
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return RecipeSerializer

    @action(detail=True, methods=['get'])
    def ingredients(self, request, id=None):
        recipe = self.get_object()
        ingredients = recipe.ingredients.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def tags(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def top(self):
        queryset = Recipe.objects.annotate(
            rating_average=models.Avg(
                'ratings__value'
            )).order_by('-rating_average')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoriteViewSet(viewsets.ViewSet):
    queryset = FavoritesList.objects.all()

    @action(detail=False, methods=['get'])
    def user_favorites(self, request):
        favorites = FavoritesList.objects.filter(user=request.user)
        serializer = RecipeSerializer(favorites.recipe, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        recipe = Recipe.objects.get(pk=pk)
        favorite = FavoritesList.objects.create(
            user=request.user,
            recipe=recipe
        )
        serializer = RecipeSerializer(favorite.recipe)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_favorite(self, request, pk=None):
        favorite = FavoritesList.objects.get(user=request.user, recipe__pk=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
