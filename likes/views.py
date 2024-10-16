from rest_framework import generics, permissions, filters
from django.db.models import Count
from rest_framework.exceptions import ValidationError
from .models import Like
from .serializers import LikeSerializer
from recipes.serializers import RecipeSerializer
from recipes.models import Recipe
from project5_api.permissions import IsOwnerOrReadOnly

class LikeListView(generics.ListAPIView):
    """
    API view to list all recipes that the authenticated user has liked.
    Allows filtering and searching on the recipe data.
    """
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return recipes that the authenticated user has liked,
        with additional annotations for like counts.
        """
        user = self.request.user
        return Recipe.objects.filter(likes__owner=user).annotate(
            likes_count=Count('likes', distinct=True)
        ).order_by('-created_at')

    # Filter and search options
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['likes_count', 'created_at']
    search_fields = ['title', 'short_description', 'ingredients']



class LikeCreateView(generics.CreateAPIView):
    """
    API view to allow users to 'like' a recipe.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Create a like instance for the authenticated 
        user and the given recipe. Raise an error if 
        the user has already liked the recipe.
        """
        user = self.request.user
        recipe = serializer.validated_data.get('recipe')

        if Like.objects.filter(owner=user, recipe=recipe).exists():
            raise ValidationError("You have already liked this recipe.")

        serializer.save(owner=user)


class LikeDeleteView(generics.DestroyAPIView):
    """
    API view to allow a user to remove a 'like' from a recipe.
    Only the owner of the like can delete it.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        """
        Override to retrieve the Like instance by the user and recipe ID.
        Raise a validation error if the like does not exist.
        """
        user = self.request.user
        recipe_id = self.kwargs.get('recipe_id')

        try:
            like = Like.objects.get(owner=user, recipe_id=recipe_id)
        except Like.DoesNotExist:
            raise ValidationError("You haven't liked this recipe yet.")
        return like

