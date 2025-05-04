from rest_framework import serializers


class PostUpdateResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
