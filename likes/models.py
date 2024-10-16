from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

class Like(models.Model):
    """
    Model representing a 'like' that a user can give to a recipe.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, 
        related_name='likes', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for the Like model, ensuring that a user can only
        like a specific recipe once and ordering likes by creation date.
        """
        unique_together = ['owner', 'recipe']
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the Like instance, showing which user
        liked which recipe.
        """
        return f'{self.owner} liked {self.recipe}'
