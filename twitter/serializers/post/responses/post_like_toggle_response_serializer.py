from rest_framework import serializers


class PostLikeToggleResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
