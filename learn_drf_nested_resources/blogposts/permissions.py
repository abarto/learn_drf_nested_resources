from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class CommentsAllowed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.allow_comments


class CommentDeleteOrUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (request.method == 'POST' or request.method == 'PATCH'):
            return obj.author == request.user
        elif request.method == 'DELETE':
            return obj.author == request.user or obj.blogpost.author == request.user

        return False
