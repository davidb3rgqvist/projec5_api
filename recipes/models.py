from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    ingredients = models.TextField(help_text="List of ingredients separated by commas")
    steps = models.TextField(help_text="Steps to make the recipe")
    cook_time = models.IntegerField(help_text="Cook time in minutes", default=30)
    difficulty = models.CharField(
    max_length=50, 
    choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], 
    default='Easy'
    )
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes_set.count()
    
    
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} - {self.content[:20]}'
