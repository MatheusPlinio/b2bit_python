from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from twitter.models import Post


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

        return Response({"liked": liked, "likes_count": post.likes.count()}, status=status.HTTP_200_OK)
