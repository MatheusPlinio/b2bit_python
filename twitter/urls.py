from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from twitter.views import *
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like'),
    path('posts/', PostListView.as_view(), name='post-list')
]
