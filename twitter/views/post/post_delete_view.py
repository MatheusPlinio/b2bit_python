from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from twitter.models import Post
from twitter.serializers.post.post_serializer import PostSerializer


@extend_schema(tags=["Post"])
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied(
                detail={"message": "Você não tem permissão para excluir este post."})
        return obj

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({"message": "Post excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
