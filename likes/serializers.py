from rest_framework import serializers
from .models import Like
from recipes.serializers import RecipeSerializer
from recipes.models import Recipe

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'owner', 'recipe', 'created_at']
