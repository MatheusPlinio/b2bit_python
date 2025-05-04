from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from twitter.serializers.auth.responses.login_response_serializer import LoginResponseSerializer, LoginErrorResponseSerializer
from twitter.serializers.user.user_serializer import UserSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user, context=self.context).data
        return data


@extend_schema(tags=["Account"],
               responses=(
    {
        201: LoginResponseSerializer,
        400: LoginErrorResponseSerializer
    }
))
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
