from django.urls import path
from twitter.views.user import UserInfoView, UserFeedView

urlpatterns = [
    path('feed/', UserFeedView.as_view(), name='feed'),
    path('<int:pk>/info/', UserInfoView.as_view(), name='info'),
]
