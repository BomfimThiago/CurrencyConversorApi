import json
from typing import Callable

from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from authentication.enums.messages import AuthMessages, ResetPasswordMessages
from authentication.models import Code
from core.models import User


def reset_password_code_request(client, email):
    """
    Make a request to the reset password code request endpoint
    Args:
        client: HTTP Client
        email: User email from which the request code will be sent
    Returns: Reset password request code endpoint response
    """
    return client.post(
        path=reverse("auth:reset-password-request-code"),
        data=json.dumps({"email": email}),
        content_type="application/json",
    )


@override_settings(DEFAULT_MESSENGER="EMAIL")
def test_successful_reset_password_email_code_request(
    client, user_1: User, format_response: Callable
) -> None:
    """Check if the `reset-password code request` endpoint sends the reset-password email with the valid code"""
    response = reset_password_code_request(client=client, email=user_1.email)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == format_response(
        ResetPasswordMessages.RESET_PASSWORD_REQUEST_CODE_SUCCESSFULLY.value
    )

    reset_password_requests = Code.objects.all()
    assert len(reset_password_requests) == 1

    reset_password_request = reset_password_requests[0]

    assert reset_password_request.user == user_1
    assert reset_password_request.was_used is False
    assert reset_password_request.code is not None

    assert len(mail.outbox) == 1
    assert reset_password_request.code in mail.outbox[0].body
    assert reset_password_request.user.email in mail.outbox[0].recipients()


def test_invalid_user_reset_password_code_request(client, user_factory):
    """Check if the `reset-password code request` endpoint gives an consistent message for a request with an invalid email"""
    user_factory()
    response = reset_password_code_request(client=client, email="invalid@ckl.io")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == AuthMessages.USER_NOT_FOUND.value

    assert Code.objects.count() == 0
