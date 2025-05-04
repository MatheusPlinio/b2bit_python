from rest_framework import serializers


class UserInfoResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    is_following = serializers.BooleanField()
