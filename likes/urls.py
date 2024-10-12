from django.urls import path
from .views import LikeCreateView, LikeDeleteView

urlpatterns = [
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('likes/<int:recipe_id>/', LikeDeleteView.as_view(), name='like-delete'),
]
