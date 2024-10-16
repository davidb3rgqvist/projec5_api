from rest_framework import serializers
from .models import Like
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    Read-only fields for the owner and references for the liked recipe.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'owner', 'recipe', 'created_at']
