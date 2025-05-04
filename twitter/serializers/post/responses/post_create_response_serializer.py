from rest_framework import serializers


class PostCreateResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
