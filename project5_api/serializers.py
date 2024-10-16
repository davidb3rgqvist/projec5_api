from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

class CurrentUserSerializer(UserDetailsSerializer):
    """
    Custom serializer to include profile information 
    with the current user's details.
    """
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        # Adding extra fields to the default user details
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )
