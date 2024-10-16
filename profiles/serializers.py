from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from recipes.models import Recipe

# Serializer for the Profile model
class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model to handle 
    serialization and deserialization of profile data, 
    including additional computed fields.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        """
        Check if the currently authenticated 
        user is the owner of the profile.
        """
        request = self.context['request']
        return request.user == obj.owner
    
    def get_following_id(self, obj):
        """
        Return the ID of the 'Follower' relationship 
        if the current user follows this profile.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_recipes_count(self, obj):
        """
        Return the number of recipes created by the profile owner.
        """
        return Recipe.objects.filter(owner=obj.owner).count()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 
            'content', 'image', 'is_owner', 'following_id', 
            'recipes_count', 'followers_count', 'following_count',
        ]
