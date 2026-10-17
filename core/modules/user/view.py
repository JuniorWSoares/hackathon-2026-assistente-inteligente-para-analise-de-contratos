from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from core.classes.base_viewset import BaseModelViewSet
from core.classes.permission import CustomPermissionClass
from core.models import User
from core.modules.user.serializer import (
    UserDetailSerializer,
    UserListSerializer,
    UserSerializer,
)
from core.modules.user.service import UserService


class UserViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermissionClass]
    serializer_class = UserSerializer
    search_fields = ["id", "email", "name"]
    ordering = ("id",)

    @property
    def router_user(self):
        if self.action in ("list", "destroy"):
            return ["ADMIN"]
        return None

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        user = self.request.user
        if user.is_authenticated and not user.is_admin_role:
            return queryset.filter(pk=user.pk)
        return queryset

    def perform_create(self, serializer):
        serializer.instance = self._service().create(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self._service().update(
            serializer.instance, serializer.validated_data
        )

    def _service(self) -> UserService:
        return UserService()