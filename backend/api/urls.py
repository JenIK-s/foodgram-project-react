from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (IngredientViewSet, RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [

]

urlpatterns += router.urls