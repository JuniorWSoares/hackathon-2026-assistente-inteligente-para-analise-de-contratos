from django.utils.translation import gettext_lazy as _

from core.models import Company


class CompanyService:
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        if password is not None:
            instance.set_password(password)

        for field, value in validated_data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance