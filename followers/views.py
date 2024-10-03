from rest_framework import generics, permissions, filters
from project5_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer

class FollowerList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    filter_backends = [
        filters.SearchFilter 
    ]
    search_fields = [
        'owner__username',
        'followed__username'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
