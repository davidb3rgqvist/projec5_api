from rest_framework import generics, permissions, filters
from project5_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer

class FollowerList(generics.ListCreateAPIView):
    """
    API view for listing and creating followers.
    Authenticated users can follow others, 
    and search filters are enabled.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['owner__username', 'followed__username']

    def perform_create(self, serializer):
        """
        Automatically assign the owner of the follow 
        relationship to the current user.
        """
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    API view for retrieving and deleting a 
    follower relationship. Only the owner of the 
    follower relationship can delete it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
