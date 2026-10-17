from uuid import uuid4

from django.core.files.storage import default_storage
from django.db import DatabaseError

from core.models import Company, Document


def create_document(*, company: Company, uploaded_file, doc_type: str | None) -> Document:
    filename = uploaded_file.name.replace("\\", "/").rsplit("/", 1)[-1][:255]
    storage_path = f"documents/{company.pk}/{uuid4().hex}.pdf"
    saved_path = default_storage.save(storage_path, uploaded_file)

    try:
        return Document.objects.create(
            company=company,
            doc_type=doc_type,
            filename=filename,
            file_path=saved_path,
        )
    except DatabaseError:
        default_storage.delete(saved_path)
        raise


def delete_document(document: Document) -> None:
    default_storage.delete(document.file_path)
    document.delete()
