from django.urls import path
from twitter.views import RegisterUserAPIView, PostCreateView, PostUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
]
