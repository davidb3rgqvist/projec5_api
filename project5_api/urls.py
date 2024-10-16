"""
URL configuration for project5_api project.
"""
from django.contrib import admin
from django.urls import path, include
from .views import root_route

urlpatterns = [
    # Root route for welcome message
    path('', root_route),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API authentication routes
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/', 
        include('dj_rest_auth.registration.urls')
    ),
    
    # App-specific routes
    path('', include('recipes.urls')),
    path('', include('likes.urls')),
    path('', include('profiles.urls')),
    path('', include('followers.urls')),
]
