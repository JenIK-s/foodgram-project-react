from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet, AuthToken

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path(
          'auth/token/login/',
          AuthToken.as_view(),
          name='login'),
]
