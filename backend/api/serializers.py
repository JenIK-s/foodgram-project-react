from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User, Follow
from recipes.models import Ingredient, Recipe, Tag



class CommonSubscribed(metaclass=serializers.SerializerMetaclass):
    """
    Класс для опредения подписки пользователя на автора.
    """
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """
        Метод обработки параметра is_subscribed подписок.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Follow.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False




class RegistrationSerializer(UserCreateSerializer, CommonSubscribed):
    """
    Создание сериализатора модели пользователя.
    """
    class Meta:
        """
        Мета параметры сериализатора модели пользователя.
        """
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'is_subscribed': {'required': False}}

    def to_representation(self, obj):
        """
        Метод представления результатов сериализатора.
        """
        result = super(RegistrationSerializer, self).to_representation(obj)
        result.pop('password', None)
        return result



class CurrentUserSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {"password": {'write_only': True}}

    # def get_is_subscribed(self, obj):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     user = request.user
    #     return Follow.objects.filter(following=obj, user=user).exists()








class CreateUserSerializer(UserCreateSerializer):
    """ Сериализатор создания пользователя. """

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]



class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


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


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tag = SimpleTagSerializer(many=True, read_only=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_list = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('tag', 'author', 'title', 'img', 'description',
                  'cooking_time',)

    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return obj.favorite_recipes.filter(user=user).exists()
    #     return False
    #
    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return obj.shopping_cart_recipes.filter(user=user).exists()
    #     return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tag = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    # is_favorite = serializers.SerializerMethodField()
    # is_in_shopping_list = serializers.SerializerMethodField()

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

    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return obj.favorite_recipes.filter(user=user).exists()
    #     return False
    #
    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return obj.shopping_cart_recipes.filter(user=user).exists()
    #     return False
