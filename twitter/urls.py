from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from twitter.views.user import (
    UserRegisterAPIView,
    CustomTokenObtainPairView,
    UserInfoView
)
from twitter.views.post import (
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostLikeToggleView,
    PostListView,
)
from twitter.views.follow import (
    FollowToggleView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('users/<int:pk>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
    path("users/<int:pk>/hover-info/", UserInfoView.as_view()),
]
