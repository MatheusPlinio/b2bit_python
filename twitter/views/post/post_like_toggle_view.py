from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from twitter.models import Post, Follow
from django.shortcuts import get_object_or_404
from twitter.tasks.update_post_likes import update_post_likes_count


@extend_schema(tags=["Post"])
class PostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        # dispara a task de atualizar contagem no cache
        update_post_likes_count.delay(post.id)

        # invalida feed de quem segue o autor + do próprio usuário
        author = post.author
        follower_ids = Follow.objects.filter(following=author) \
                                     .values_list('follower_id', flat=True)
        # também invalida o feed do autor se quiser refletir o próprio like
        keys_to_clear = set(follower_ids) | {user.id, author.id}
        for uid in keys_to_clear:
            cache.delete(f"user_feed_{uid}")

        # retorna imediatamente a contagem
        likes_count = cache.get(f"post_likes_count_{post.id}")
        if likes_count is None:
            likes_count = post.likes.count()

        return Response(status=status.HTTP_200_OK)
