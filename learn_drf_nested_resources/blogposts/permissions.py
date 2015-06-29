from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class CommentDeleteOrUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (request.method == 'POST' or request.method == 'PATCH'):
            return obj.author == request.user
        elif request.method == 'DELETE':
            return obj.author == request.user or obj.blogpost.author == request.user
        
        return False
