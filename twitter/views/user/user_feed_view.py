from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from ...tasks import rebuild_user_feed_cache


@extend_schema(tags=["Account"])
class UserFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"user_feed_{user.id}"
        cached = cache.get(cache_key)

        if cached is not None:
            return Response(cached)

        rebuild_user_feed_cache.delay(user.id)
        return Response([], status=202)
