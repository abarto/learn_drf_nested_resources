from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Blogpost, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import BlogpostSerializer, CommentSerializer


class BlogpostViewSet(ModelViewSet):
    serializer_class = BlogpostSerializer
    queryset = Blogpost.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
