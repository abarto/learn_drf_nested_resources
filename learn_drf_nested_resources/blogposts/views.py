from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Blogpost, Comment
from .permissions import (
    IsAuthorOrReadOnly, CommentDeleteOrUpdatePermission, CommentsAllowed
)
from .serializers import BlogpostSerializer, CommentSerializer


class BlogpostViewSet(ModelViewSet):
    serializer_class = BlogpostSerializer
    queryset = Blogpost.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, CommentDeleteOrUpdatePermission)


class NestedCommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, CommentsAllowed)

    def get_blogpost(self, request, blogpost_pk=None):
        """
        Look for the referenced blogpost
        """
        # Check if the referenced blogpost exists
        blogpost = get_object_or_404(Blogpost.objects.all(), pk=blogpost_pk)

        # Check permissions
        self.check_object_permissions(self.request, blogpost)

        return blogpost

    def create(self, request, *args, **kwargs):
        self.get_blogpost(request, blogpost_pk=kwargs['blogpost_pk'])

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            blogpost_id=self.kwargs['blogpost_pk']
        )

    def get_queryset(self):
        return Comment.objects.filter(blogpost=self.kwargs['blogpost_pk'])

    def list(self, request, *args, **kwargs):
        self.get_blogpost(request, blogpost_pk=kwargs['blogpost_pk'])

        return super().list(request, *args, **kwargs)
