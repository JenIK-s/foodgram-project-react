from .imports import *

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
        purchases = ShoppingList.objects.filter(user=request.user)
        file = 'shopping-list.txt'
        str_list = []
        with open(file, 'w') as f:
            for elem in purchases:
                recipe = elem.recipe
                result_str = str(
                    f'Автор рецепта: {recipe.author}\n'
                    + f'Название рецепта: {recipe.name}\n'
                    + f'Описание: {recipe.text}\n'
                )

                f.write(result_str + '\n')

        return FileResponse(open(file, 'rb'), as_attachment=True)
