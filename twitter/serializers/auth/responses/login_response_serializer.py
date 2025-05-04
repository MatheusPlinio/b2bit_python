from rest_framework import serializers
from twitter.serializers.user.user_serializer import UserSerializer


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class LoginErrorResponseSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
