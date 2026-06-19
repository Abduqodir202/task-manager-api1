from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView

urlpatterns = [
    path('api/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
]