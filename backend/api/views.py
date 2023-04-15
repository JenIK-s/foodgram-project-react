from rest_framework import viewsets
from ..recipes.models import Recipe, Ingredient, Tag, FavoritesList
from .serializers import RecipeSerializer, IngredientSerializer, TagSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


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
        favorite = FavoritesList.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeSerializer(favorite.recipe)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_favorite(self, request, pk=None):
        favorite = FavoritesList.objects.get(user=request.user, recipe__pk=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
