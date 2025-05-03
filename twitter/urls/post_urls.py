from django.urls import path
from twitter.views.post import (
    PostCreateView, PostUpdateView, PostDeleteView,
    PostLikeToggleView, PostListView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like'),
]
