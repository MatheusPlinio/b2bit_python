from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema
from ...models import Post
from ...serializers.post.post_serializer import PostSerializer


@extend_schema(tags=["Post"])
class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied(
                "Você não tem permissão para editar este post.")
        return obj
