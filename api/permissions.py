from rest_framework.permissions import BasePermission, SAFE_METHODS


class Usercreation(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True
        elif obj == request.user:
            return True
        return False

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            if request.user.is_superuser:
                return True
            else:
                return False
        else:
            return True


class Articlecreation(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.author == request.user or request.user.is_superuser:
            return True
        else:
            return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        else:
            return False
