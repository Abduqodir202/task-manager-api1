from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS - hamma uchun ochiq
        if request.method in SAFE_METHODS:
            return True

        # POST, PUT, PATCH, DELETE - login qilgan user uchun
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # GET - hamma ko'rishi mumkin
        if request.method in SAFE_METHODS:
            return True

        # PUT, PATCH, DELETE - faqat post egasi
        return obj.author == request.user