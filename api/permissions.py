from rest_framework.permissions import BasePermission


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return request.user == obj.author
        return super().has_object_permission(request, view, obj)
