from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Read for all; write only for the owner (author).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj.author must exist on both Post and Comment
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)
