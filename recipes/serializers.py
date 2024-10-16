from rest_framework import serializers
from .models import Recipe, Comment
from likes.models import Like
from profiles.models import Profile

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model, 
    including related profile details.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = Comment
        fields = [
            'id', 'recipe', 'owner', 'content', 'created_at',
            'updated_at', 'is_owner', 'profile_id', 'profile_image'
        ]

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the comment.
        """
        request = self.context.get('request')
        return request.user == obj.owner


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model, including 
    related fields like comments and likes count.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'owner', 'title', 'short_description', 'ingredients', 
            'steps', 'cook_time', 'difficulty', 'image', 
            'created_at', 'updated_at', 'likes_count', 'is_liked', 'comments'
        ]

    def get_likes_count(self, obj):
        """
        Return the total number of likes for the recipe.
        """
        return obj.likes.count()

    def get_is_liked(self, obj):
        """
        Check if the current user has liked the recipe.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(owner=user, recipe=obj).exists()
        return False
