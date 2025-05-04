from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from twitter.models import User, Follow
from twitter.serializers.user.responses.user_info_response_serializer import UserInfoResponseSerializer


@extend_schema(tags=["Account"], responses=({200: UserInfoResponseSerializer}))
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
