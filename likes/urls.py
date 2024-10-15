from django.urls import path
from .views import LikeCreateView, LikeDeleteView, LikeListView

urlpatterns = [
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('likes/list/', LikeListView.as_view(), name='like-list'),
    path('likes/<int:recipe_id>/', LikeDeleteView.as_view(), name='like-delete'),
]
