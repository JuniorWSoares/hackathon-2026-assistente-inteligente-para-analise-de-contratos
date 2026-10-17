import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def _normalize(self, email):
        return self.normalize_email((email or "").strip().lower())

    def create_user(self, email, password=None):
        email = self._normalize(email)
        if not email:
            raise ValueError(_("Users must have an email"))

        user = self.model(
            email=email,
            is_active=True,
            role=User.Role.USER,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)

        user.is_staff = True
        user.role = User.Role.ADMIN
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, Base):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  
    is_staff = models.BooleanField(
        default=False,
        help_text="Designa se o usuário pode acessar o Django Admin (/admin/).",
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        help_text="Papel na API: ADMIN ou USER.",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return bool(self.is_staff)

    def has_module_perms(self, app_label):
        return bool(self.is_staff)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.updated_at = timezone.now()
        self.save(update_fields=["is_active", "updated_at"])