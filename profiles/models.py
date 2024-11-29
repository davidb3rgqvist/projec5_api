from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Profile model to extend user data with additional fields
class Profile(models.Model):
    """
    A model representing a user profile. Each user has one profile.
    The profile includes fields for name, content, image, email, and age.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_sqbwns'
    )
    # email = models.EmailField(max_length=255, unique=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        blank=True, null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


# Signal to automatically create a profile for each new user
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile whenever a new User is created.
    """
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
