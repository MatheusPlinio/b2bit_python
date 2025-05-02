from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ...models import User
from ...serializers.user.user_serializer import UserSerializer


class FollowingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(followers__follower_id=user_id)
