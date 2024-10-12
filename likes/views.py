from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Like
from .serializers import LikeSerializer
from project5_api.permissions import IsOwnerOrReadOnly


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        recipe = serializer.validated_data['recipe']
        if Like.objects.filter(owner=user, recipe=recipe).exists():
            raise ValidationError("You have already liked this recipe.")
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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
