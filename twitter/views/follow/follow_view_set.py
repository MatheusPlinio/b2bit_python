from ...models import Post
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ...models import Follow
from ...serializers.user.follow_serializer import FollowSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
