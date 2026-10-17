from rest_framework import serializers
from core.models import Company
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

COMPANY_FIELDS = (
    "id",
    "cnpj",
    "email",
    "legal_name",
    "cnae_primary",
    "company_size",
    "founded_on",
    "address_city",
    "address_state",
    "confirmed",
    "created_at",
)
READ_ONLY_FIELDS = ("id", "cnpj", "created_at")


class CompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Company
        fields = COMPANY_FIELDS + ("password",)
        read_only_fields = READ_ONLY_FIELDS

    def validate_password(self, value):
        validate_password(value, user=self.instance)
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": [_("Senha é obrigatória.")]})
        return attrs


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = COMPANY_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = COMPANY_FIELDS
        read_only_fields = READ_ONLY_FIELDS
