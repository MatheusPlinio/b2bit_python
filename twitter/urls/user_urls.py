from django.urls import path
from twitter.views.user import UserInfoView

urlpatterns = [
    path('<int:pk>/info/', UserInfoView.as_view(), name='info'),
]
