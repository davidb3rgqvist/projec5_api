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
