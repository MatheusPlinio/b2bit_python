from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from ...models import User, Follow


@extend_schema(tags=["Follow"])
class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)

        if request.user == target_user:
            return Response({'detail': "You cannot follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=target_user
        )

        if not created:
            follow.delete()

            cache.delete(f"user_followers_count_{target_user.id}")
            cache.delete(f"user_feed_{request.user.id}")

            return Response({'status': 'unfollowed'})

        cache.delete(f"user_followers_count_{target_user.id}")
        cache.delete(f"user_feed_{request.user.id}")

        return Response({'status': 'followed'})
