from django.urls import path
from twitter.views.follow import FollowToggleView

urlpatterns = [
    path('<int:pk>/', FollowToggleView.as_view(), name='follow-toggle')
]