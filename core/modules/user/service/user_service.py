from django.utils.translation import gettext_lazy as _

from core.models import User


class UserService:
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data, is_active=True, role=User.Role.USER, is_staff=False)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        if password is not None:
            instance.set_password(password)

        for field, value in validated_data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance