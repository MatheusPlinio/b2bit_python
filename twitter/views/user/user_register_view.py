from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field, extend_schema
from ...serializers.user.register_serializer import UserRegistrationSerializer
from twitter.serializers.auth.responses.register_response_serializer import UserRegistrationErrorResponseSerializer, RegisterResponseSerializer


@extend_schema(tags=["Account"],
               responses=(
    {
        201: RegisterResponseSerializer,
        400: UserRegistrationErrorResponseSerializer
    }
))
class UserRegisterAPIView(APIView):
    permission_classes = []
    serializer_class = UserRegistrationSerializer

    @extend_schema_field(UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = UserRegistrationSerializer(user)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
