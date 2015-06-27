from rest_framework.viewsets import ModelViewSet

from .models import Blogpost, Comment
from .serializers import BlogpostSerializer, CommentSerializer


class BlogpostViewSet(ModelViewSet):
    serializer_class = BlogpostSerializer
    queryset = Blogpost.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
