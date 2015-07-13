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
from .permissions import IsAuthorOrReadOnly, CommentDeleteOrUpdatePermission
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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_blogpost(self, request, blogpost_pk=None):
        """
        Look for the referenced blogpost
        """
        # Check if the referenced blogpost exists
        blogpost = get_object_or_404(Blogpost.objects.all(), pk=blogpost_pk)

        # Check permissions
        self.check_object_permissions(self.request, blogpost)

        return blogpost

    def create(self, request, *args, blogpost_pk=None, **kwargs):
        blogpost = self.get_blogpost(request, blogpost_pk=blogpost_pk)

        # Check if comments are allowed
        if not blogpost.allow_comments:
            raise PermissionDenied

        # Proceed as usual

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            author=self.request.user,
            blogpost=blogpost
        )

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, blogpost_pk=None, **kwargs):
        blogpost = self.get_blogpost(request, blogpost_pk=blogpost_pk)

        queryset = self.filter_queryset(
            self.get_queryset().filter(blogpost=blogpost)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
