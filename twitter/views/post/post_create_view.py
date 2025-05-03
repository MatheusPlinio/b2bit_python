from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema
from ...models import Post
from ...serializers.post.post_serializer import PostSerializer


@extend_schema(tags=["Post"])
class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
