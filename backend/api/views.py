from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.contrib.auth import get_user_model

from .permissions import IsReadOnly
from recipes.models import Recipe, Ingredient, Tag, FavoritesList
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
    CurrentUserSerializer,
)
from rest_framework.permissions import (
    AllowAny
)

from djoser.views import UserViewSet


User = get_user_model()



from rest_framework.permissions import IsAuthenticated 


    
class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    search_fields = ('username', 'email')
    permission_classes = (IsAuthenticated,) 
    # permission_classes = [AllowAny, ]
    



from .permissions import IsAuthorAdminOrReadOnly

from .serializers import RecipeListSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')

    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthorAdminOrReadOnly, ]


    filter_backends = [DjangoFilterBackend]
    # filterset_fields = [
    #     'author',
    #     'tag',
    # ]
    # search_fields = ['name', 'tags__name']
    # lookup_field = 'id'

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
    def tag(self, request):
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
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
