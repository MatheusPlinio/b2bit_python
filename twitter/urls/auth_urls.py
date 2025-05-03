from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from twitter.views.user import UserRegisterAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
