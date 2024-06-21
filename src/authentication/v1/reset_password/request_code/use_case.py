from django.conf import settings
from django.core.mail import send_mail

from authentication.exceptions.user import UserNotFound
from authentication.models import Code
from core.models import User
from core.utils.use_cases.base import BaseUseCase


class ResetPasswordRequestCodeUseCase(BaseUseCase):
    def _notify_request(self, reset_password_request: Code) -> None:
        """
        Send the password request validation code through the default messenger
        Params:
            reset_password_request: The instance with the reset password request data
        """
        send_mail(
            subject="Password reset request",
            message=f"Hi, This is your password reset code: {reset_password_request.code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reset_password_request.user.email],
            fail_silently=False,
        )

    def _get_user_by_email(self, email: str) -> User:
        """
        Get the user by its email
        Params:
            email: The email of the user that is going to be retrieved
        Returns: The user with the email field
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserNotFound()

    def execute(self, email: str) -> None:
        """
        Create a reset password request instance and send its validation code to the user
        Params:
            email: The email address of the user that will have its password reseted
        """
        user = self._get_user_by_email(email)
        reset_password_request = Code.objects.create(
            user=user, type=Code.RESET_PASSWORD_REQUEST_TYPE
        )
        self._notify_request(reset_password_request)
