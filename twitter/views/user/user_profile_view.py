from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from twitter.serializers.user.user_profile_serializer import UserProfileSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

User = get_user_model()


@extend_schema(tags=["Account"])
class UserProfileDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
