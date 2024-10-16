from django.db.models import Count
from rest_framework import generics, permissions, filters
from .models import Profile
from .serializers import ProfileSerializer
from project5_api.permissions import IsOwnerOrReadOnly

# List all profiles and include aggregated data
class ProfileList(generics.ListAPIView):
    """
    View for listing all profiles with annotated 
    data such as recipe counts, followers count, and 
    following count. Supports filtering and searching.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    ordering_fields = [
        'recipes_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]
    search_fields = [
        'owner__username',
        'name',
        'content',
    ]

    def get_serializer_context(self):
        """
        Provide request context to the serializer.
        """
        return {'request': self.request}

# Detail view for retrieving or updating a single profile
class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific profile.
    Only the profile owner can update their own profile.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        """
        Provide request context to the serializer.
        """
        return {'request': self.request}

    def perform_update(self, serializer):
        """
        Save the updated profile data 
        with the current user as the owner.
        """
        serializer.save(owner=self.request.user)
        
# Delete view for removing a profile and its associated user
class ProfileDelete(generics.DestroyAPIView):
    """
    View for deleting a specific profile and the associated user account.
    Only the profile owner can delete their own profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        """
        Provide request context to the serializer.
        """
        return {'request': self.request}

    def perform_destroy(self, instance):
        """
        Custom deletion logic to delete the profile and the associated user.
        """
        
        user = instance.owner
        user.delete()

        instance.delete()
