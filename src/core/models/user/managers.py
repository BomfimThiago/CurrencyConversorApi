from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from core.models import User  # noqa: F401


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def create_user(self, email: str, password: str, **extra_fields: dict):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email: str, password: str, **extra_fields: dict):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
