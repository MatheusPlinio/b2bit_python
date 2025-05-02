from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ...models import User, Follow


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        is_following = Follow.objects.filter(
            follower=request.user, following=user).exists()

        return Response({
            "id": user.id,
            "username": user.username,
            "is_following": is_following
        })
