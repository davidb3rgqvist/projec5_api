# Permission class to restrict update and delete actions only to the owner of the object
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS like GET are allowed for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow the owner to edit/delete the object
        return obj.owner == request.user
