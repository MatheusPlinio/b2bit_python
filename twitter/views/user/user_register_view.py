from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field, extend_schema
from ...serializers.user.register_serializer import UserRegistrationSerializer


@extend_schema(tags=["Account"])
class UserRegisterAPIView(APIView):
    permission_classes = []
    serializer_class = UserRegistrationSerializer

    @extend_schema_field(UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = UserRegistrationSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
