from django.urls import path
from profiles import views

# URL patterns for Profile views
urlpatterns = [
     path('profiles/', views.ProfileList.as_view(), 
         name='profile-list'),
     path('profiles/<int:pk>/', views.ProfileDetail.as_view(), 
         name='profile-detail'),
     path('profiles/<int:pk>/', views.ProfileDelete.as_view(), 
          name='profile-delete'),
]