from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ...models import Post
from ...serializers.post.post_serializer import PostSerializer
from ...permissions import IsOwnerOrReadOnly


class PostListView(ListAPIView):
    queryset = Post.objects.select_related(
        'author').all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
