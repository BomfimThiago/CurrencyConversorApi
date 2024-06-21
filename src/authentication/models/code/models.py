from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from authentication.utils.secrets import generate_code
from core.models import User
from core.utils.models.base import BaseModel


class Code(BaseModel):
    RESET_PASSWORD_REQUEST_TYPE = "RESET_PASSWORD_REQUEST"
    USER_CONFIRMATION_TYPE = "USER_CONFIRMATION"
    CODE_TYPES = (
        (RESET_PASSWORD_REQUEST_TYPE, RESET_PASSWORD_REQUEST_TYPE),
        (USER_CONFIRMATION_TYPE, USER_CONFIRMATION_TYPE),
    )

    user = models.ForeignKey(
        User,
        related_name="code_tokens",
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this"),
    )
    code = models.CharField(_("Code"), max_length=6, default=generate_code)
    type = models.CharField(_("Type"), max_length=25, choices=CODE_TYPES)
    was_used = models.BooleanField(_("Was already used?"), default=False)

    def __str__(self):
        return f"{self.user}"

    @property
    def is_eligible_for_reset(self):
        """Is code still valid?"""
        return (
            not self.was_used
            and (timezone.now() - self.created) < settings.FORGOT_TIME_EXPIRATION_TIME
        )

    class Meta:
        verbose_name = _("Code")
        ordering = ("-created",)
