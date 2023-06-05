from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User, Follow
from recipes.models import Ingredient, Recipe, Tag

class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'write_only': True}}


class CurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_subscribed',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(following=obj, author=user).exists()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже отслеживаете обновления данного автора'
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя'
            )
        return data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class SimpleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'color_key')




from recipes.models import IngredientInRecipe


class IngredientRecipeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', )

class RecipeListSerializer(serializers.ModelSerializer):
    tags = SimpleTagSerializer(many=True)
    author = CurrentUserSerializer()
    ingredients = IngredientRecipeListSerializer(
        many=True,
        source='ingredient_recipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')









class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tag = SimpleTagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('tag', 'author', 'title', 'img', 'description',
                  'cooking_time',)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorite_recipes.filter(user=user).exists()
        return False
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.shopping_cart_recipes.filter(user=user).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tag = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tag',
            'author',
            'ingredients',
            'title',
            'img',
            'description',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorite_recipes.filter(user=user).exists()
        return False
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.shopping_cart_recipes.filter(user=user).exists()
        return False
