from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (FavoritesList, Ingredient, IngredientInRecipe, Recipe,
                          ShoppingList, Tag)
from users.models import User, Subscription
from drf_extra_fields.fields import Base64ImageField
from users.serializers import CurrentUserSerializer

class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='author.id')
    email = serializers.EmailField(source='author.email')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'recipes', 'is_subscribed', 'recipes_count',)

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = SubscribeRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit',)


class RecipeSerializer(serializers.ModelSerializer):
    author = CurrentUserSerializer()
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='amount_ingredient'
    )
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request =  self.context.get('request')
        return FavoritesList.objects.filter(
            user_id=request.user.id,
            recipe_id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request =  self.context.get('request')
        return ShoppingList.objects.filter(
            user_id=request.user.id,
            recipe_id=obj.id
        ).exists()


class RecipeAddSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate_ingredients_and_tags(self, data):
        if not data['tags']:
            raise serializers.ValidationError(
                'Выберите хотябы один тег'
            )
        if not data['ingredients']:
            raise serializers.ValidationError(
                'Выберите хотябы один ингридиент'
            )
        for ingredient in data['ingredients']:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1!')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
        return recipe

    def update(self, recipe, validated_data):
        recipe.ingredients.clear()
        recipe.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().update(recipe, validated_data)
        # return self.add_ingredients_and_tags(
        #     tags, ingredients, recipe
        # )
        recipe.tags.set(tags)
        for ingredient in ingredients:
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
        return recipe