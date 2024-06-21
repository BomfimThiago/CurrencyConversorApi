import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = None  # Remove username field
    email = models.EmailField(_("Email address"), unique=True)
    full_name = models.CharField(_("Full name"), max_length=60, blank=True)

    # Permissions
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is admin"), default=False)

    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
