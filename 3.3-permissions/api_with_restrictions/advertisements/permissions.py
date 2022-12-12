from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.is_staff


class NotOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user != obj.creator
