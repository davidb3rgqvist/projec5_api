from rest_framework import generics, permissions, filters
from django.db.models import Count
from rest_framework.exceptions import ValidationError
from .models import Like
from .serializers import LikeSerializer
from recipes.models import Recipe
from project5_api.permissions import IsOwnerOrReadOnly


class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(likes__owner=user).annotate(
            likes_count=Count('likes', distinct=True)
        ).order_by('-created_at')
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    
    ordering_fields = [
        'likes_count',
        'created_at',
    ]
    
    search_fields = [
        'title',
        'description',
        'ingredients',
    ]


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        recipe = serializer.validated_data['recipe']
        
        if Like.objects.filter(owner=user, recipe=recipe).exists():
            raise ValidationError("You have already liked this recipe.")
        
        serializer.save(owner=user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        """
        Override the get_object method to retrieve the like based on the user and recipe.
        """
        user = self.request.user
        recipe_id = self.kwargs.get('recipe_id')

        try:
            like = Like.objects.get(owner=user, recipe_id=recipe_id)
        except Like.DoesNotExist:
            raise ValidationError("You haven't liked this recipe yet.")
        return like
