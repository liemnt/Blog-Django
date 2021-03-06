from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object"
    my_safe_method = ["PUT", "GET","DELETE"]

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
