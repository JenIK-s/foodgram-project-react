from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserViewSet

app_name = 'api'

router_1 = DefaultRouter()
router_1.register('tags', TagViewSet)
router_1.register('ingredients', IngredientViewSet)
router_1.register('recipes', RecipeViewSet)
router_1.register('users', UserViewSet)

urlpatterns = [
    path('', include(router_1.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
