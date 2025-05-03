from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
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
            return Response({'status': 'unfollowed'})

        return Response({'status': 'followed'})
