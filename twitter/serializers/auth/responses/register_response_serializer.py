from rest_framework import serializers
from twitter.serializers.user.user_serializer import UserSerializer


class RegisterResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserRegistrationErrorResponseSerializer(serializers.Serializer):
    email = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    username = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    password = serializers.ListField(
        child=serializers.CharField(), required=False
    )
