from ..models import Post
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Follow, User
from ..serializers import user_serializer


class FollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = User.objects.get(pk=pk)
        if user_to_follow != request.user:
            Follow.objects.get_or_create(
                follower=request.user, following=user_to_follow)
            return Response({'status': 'following'})
        return Response({'status': 'cannot follow yourself'}, status=400)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = User.objects.get(pk=pk)
        follow_instance = Follow.objects.filter(
            follower=request.user, following=user_to_unfollow)
        if follow_instance.exists():
            follow_instance.delete()
            return Response({'status': 'unfollowed'})
        return Response({'status': 'not following this user'}, status=400)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = User.objects.get(pk=pk)
        followers = user.followers.all()
        serializer = user_serializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = User.objects.get(pk=pk)
        following = user.following.all()
        serializer = user_serializer(following, many=True)
        return Response(serializer.data)
