from django.urls import path
from .views import LikeCreateView, LikeDeleteView

urlpatterns = [
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('likes/<int:pk>/', LikeDeleteView.as_view(), name='like-delete'),
]
