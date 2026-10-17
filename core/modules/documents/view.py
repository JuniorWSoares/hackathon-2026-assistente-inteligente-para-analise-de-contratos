from rest_framework.permissions import IsAuthenticated

from core.classes.base_viewset import BaseModelViewSet
from core.classes.permission import CustomPermissionClass
from core.models import Document
from core.modules.documents.serializer import DocumentSerializer
from core.modules.documents.service import delete_document


class DocumentViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermissionClass]
    serializer_class = DocumentSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return Document.objects.filter(company=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

    def perform_destroy(self, instance):
        delete_document(instance)
