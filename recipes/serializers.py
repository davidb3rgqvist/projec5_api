from rest_framework import serializers
from .models import Recipe, Comment
from profiles.models import Profile

class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'owner', 'title', 'short_description', 'ingredients', 'steps', 'image', 'created_at', 'updated_at', 'likes_count', 'is_liked']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'owner', 'content', 'created_at', 'updated_at', 'is_owner', 'profile_id', 'profile_image']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner
