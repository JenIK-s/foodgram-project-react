from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserViewSet

app_name = 'api'

router_3_12_4 = DefaultRouter()
router_3_12_4.register('tags', TagViewSet)
router_3_12_4.register('ingredients', IngredientViewSet)
router_3_12_4.register('recipes', RecipeViewSet)
router_3_12_4.register('users', UserViewSet)

urlpatterns = [
    path('', include(router_3_12_4.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
