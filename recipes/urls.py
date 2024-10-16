from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, CommentViewSet, RankedLikedRecipesView

# Define router for Recipe and Comment ViewSets
router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'comments', CommentViewSet)

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('ranked-liked-recipes/', RankedLikedRecipesView.as_view(), 
         name='ranked-liked-recipes'),
]
