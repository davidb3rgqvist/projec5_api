from rest_framework import serializers
from .models import Like 
from recipes.serializers import RecipeSerializer

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'owner', 'recipe', 'created_at']