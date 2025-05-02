from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from ...models import Post
from ...serializers.post.post_serializer import PostSerializer


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
