from rest_framework import serializers
from core.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = (
            "id",
            "profile_image",
            "email",
            "name",
            "password",
            "is_staff",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "role", "is_active", "created_at", "updated_at")
        
    def validate_password(self, value):
        validate_password(value, user=self.instance)
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": [_("Senha é obrigatória.")]})
        return attrs
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "profile_image",
            "email",
            "name",
            "is_staff",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "role", "is_active", "created_at", "updated_at")
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "profile_image",
            "email",
            "name",
            "is_staff",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "role", "is_active", "created_at", "updated_at")