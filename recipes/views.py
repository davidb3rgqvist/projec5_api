from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Recipe, Comment
from .serializers import RecipeSerializer, CommentSerializer
from project5_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Recipe CRUD operations, with filtering, 
    searching, and listing capabilities. Recipes can be filtered 
    by owner and title, and searched by title, ingredients, 
    and short description.
    """
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticated, 
        IsOwnerOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title', 'ingredients', 'short_description']

    def perform_create(self, serializer):
        """
        Set the owner of the recipe to the current user upon creation.
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure the owner of the recipe remains the same upon update.
        """
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def by_profile(self, request, pk=None):
        """
        Custom action to retrieve recipes by profile ID.
        """
        profile_id = request.query_params.get('profile_id')
        if profile_id:
            recipes = Recipe.objects.filter(owner__profile__id=profile_id)
            serializer = self.get_serializer(recipes, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Profile ID not provided.'}, status=400)


class RankedLikedRecipesView(APIView):
    """
    API view to retrieve a list of recipes liked by the 
    current user, ranked by the number of likes in descending order.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get the recipes liked by the current user, 
        ranked by the number of likes.
        """
        user = request.user
        liked_recipes = Recipe.objects.filter(likes__owner=user).distinct()
        ranked_recipes = sorted(
            liked_recipes, 
            key=lambda recipe: recipe.likes.count(), 
            reverse=True
        )

        serializer = RecipeSerializer(
            ranked_recipes, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Comment CRUD operations.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated, 
        IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        """
        Set the owner of the comment to the current user upon creation.
        """
        serializer.save(owner=self.request.user)
