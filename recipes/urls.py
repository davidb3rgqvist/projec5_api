from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
