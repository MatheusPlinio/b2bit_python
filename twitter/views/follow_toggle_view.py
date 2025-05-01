from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Follow


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_follow = Follow.objects.filter(follower=request.user, following=target_user)

        if existing_follow.exists():
            existing_follow.delete()
            return Response({'detail': 'Unfollowed'}, status=status.HTTP_200_OK)
        else:
            Follow.objects.create(follower=request.user, following=target_user)
            return Response({'detail': 'Followed'}, status=status.HTTP_200_OK)
