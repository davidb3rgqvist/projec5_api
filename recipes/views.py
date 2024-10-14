from rest_framework import viewsets, permissions
from .models import Recipe, Comment
from .serializers import RecipeSerializer, CommentSerializer
from project5_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title', 'ingredients', 'short_description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def by_profile(self, request, pk=None):
        profile_id = request.query_params.get('profile_id')
        if profile_id:
            recipes = Recipe.objects.filter(owner__profile__id=profile_id)
            serializer = self.get_serializer(recipes, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Profile ID not provided.'}, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)