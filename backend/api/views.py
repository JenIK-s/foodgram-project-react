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
    permission_classes = (AllowAny,)
    



from .permissions import IsAuthorAdminOrReadOnly

# from .serializers import RecipeListSerializer

# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all().order_by('-id')
#     permission_classes = (IsReadOnly)
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = [
#         'author',
#         'tags',
#         'is_favorited',
#         'is_in_shopping_list'
#     ]
#     search_fields = ['name', 'tags__name']
#     lookup_field = 'id'

#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return RecipeDetailSerializer
#         return RecipeSerializer

#     @action(detail=True, methods=['get'])
#     def ingredients(self, request, id=None):
#         recipe = self.get_object()
#         ingredients = recipe.ingredients.all()
#         serializer = IngredientSerializer(ingredients, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'])
#     def tags(self, request):
#         tags = Tag.objects.all()
#         serializer = TagSerializer(tags, many=True)
#         return Response(serializer.data)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     @action(detail=False, methods=['get'])
#     def top(self):
#         queryset = Recipe.objects.annotate(
#             rating_average=models.Avg(
#                 'ratings__value'
#             )).order_by('-rating_average')
#         page = self.paginate_queryset(queryset)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)


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



# from .serializers import RecipeDetailSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     permission_classes = (IsAuthorOrReadOnly,)
#     pagination_class = LimitPageNumberPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = RecipeFilter

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return RecipeSerializer
#         return RecipePostSerializer

    # def post_del_recipe(self, request, pk, database):
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     if request.method == 'POST':
    #         if not database.objects.filter(
    #                 user=self.request.user,
    #                 recipe=recipe).exists():
    #             database.objects.create(
    #                 user=self.request.user,
    #                 recipe=recipe)
    #             serializer = SubscribeRecipeSerializer(recipe)
    #             return Response(serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #         text = 'errors: Объект уже в списке.'
    #         return Response(text, status=status.HTTP_400_BAD_REQUEST)

    #     if request.method == 'DELETE':
    #         if database.objects.filter(
    #                 user=self.request.user,
    #                 recipe=recipe).exists():
    #             database.objects.filter(
    #                 user=self.request.user,
    #                 recipe=recipe).delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         text = 'errors: Объект не в списке.'
    #         return Response(text, status=status.HTTP_400_BAD_REQUEST)

    #     else:
    #         text = 'errors: Метод обращения недопустим.'
    #         return Response(text, status=status.HTTP_400_BAD_REQUEST)

    # @action(
    #     detail=True,
    #     methods=['POST', 'DELETE'],
    #     permission_classes=(IsAuthenticated,)
    # )
    # def favorite(self, request, pk=None):
    #     return self.post_del_recipe(request, pk, FavoriteRecipe)

    # @action(
    #     detail=True,
    #     methods=['POST', 'DELETE'],
    #     permission_classes=(IsAuthenticated,)
    # )
    # def shopping_cart(self, request, pk):
    #     return self.post_del_recipe(request, pk, ShoppingCart)

    # @action(
    #     detail=False,
    #     methods=['GET'],
    #     permission_classes=(IsAuthenticated,)
    # )
    # def download_shopping_cart(self, request):
    #     user = request.user
    #     purchases = ShoppingCart.objects.filter(user=user)
    #     file = 'shopping-list.txt'
    #     with open(file, 'w') as f:
    #         shop_cart = dict()
    #         for purchase in purchases:
    #             ingredients = IngredientAmount.objects.filter(
    #                 recipe=purchase.recipe.id
    #             )
    #             for r in ingredients:
    #                 i = Ingredient.objects.get(pk=r.ingredient.id)
    #                 point_name = f'{i.name} ({i.measurement_unit})'
    #                 if point_name in shop_cart.keys():
    #                     shop_cart[point_name] += r.amount
    #                 else:
    #                     shop_cart[point_name] = r.amount

    #         for name, amount in shop_cart.items():
    #             f.write(f'* {name} - {amount}\n')

    #     return FileResponse(open(file, 'rb'), as_attachment=True)