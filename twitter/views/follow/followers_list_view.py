from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from ...models import User
from ...serializers.user.user_serializer import UserSerializer


@extend_schema(tags=["Follow"])
class FollowersListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(following__following_id=user_id)
