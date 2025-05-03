from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from twitter.models import Post
from twitter.tasks.update_post_likes import update_post_likes_count


@extend_schema(tags=["Post"])
class PostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        update_post_likes_count.delay(post.id)

        likes_count = cache.get(f"post_likes_count_{post.id}")
        if likes_count is None:
            likes_count = post.likes.count()

        return Response({
            "liked": liked,
            "likes_count": likes_count
        }, status=status.HTTP_200_OK)
