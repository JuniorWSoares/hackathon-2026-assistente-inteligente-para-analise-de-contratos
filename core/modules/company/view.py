from rest_framework.permissions import IsAuthenticated

from core.classes.base_viewset import BaseModelViewSet
from core.classes.permission import CustomPermissionClass
from core.models import Company
from core.modules.company.serializer import (
    CompanyDetailSerializer,
    CompanyListSerializer,
    CompanySerializer,
)
from core.modules.company.service import CompanyService


class CompanyViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermissionClass]
    serializer_class = CompanySerializer
    search_fields = ["id", "email", "cnpj", "legal_name"]
    ordering = ("id",)
    # Cadastro é feito em /auth/register/, junto com a empresa.
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        if self.action == "retrieve":
            return CompanyDetailSerializer
        return CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(pk=self.request.user.pk)

    def perform_update(self, serializer):
        serializer.instance = self._service().update(
            serializer.instance, serializer.validated_data
        )

    def _service(self) -> CompanyService:
        return CompanyService()