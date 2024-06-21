import json

from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

from authentication.enums.messages import ResetPasswordMessages


def reset_password(client, uidb64, token, password):
    """
    Make a request to the reset password endpoint
    Args:
        client: HTTP Client
        uidb64: User's encrypted primary key
        token: Expirable token that authenticates the user
        password: New password
    Returns: Reset password validate code endpoint response
    """
    return client.post(
        path=reverse("auth:reset-password", kwargs={"uidb64": uidb64, "token": token}),
        data=json.dumps({"password": password}),
        content_type="application/json",
    )


def test_successful_reset_password(
    client,
    user_1,
    user_1_reset_password_data,
    format_response,
):
    """Check if a user with valid request data can reset its password"""
    uidb64, token = user_1_reset_password_data
    new_password = "Valid Password"
    response = reset_password(
        client=client, uidb64=uidb64, token=token, password=new_password
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == format_response(
        ResetPasswordMessages.RESET_PASSWORD_SUCCESSFULLY.value
    )
    user = authenticate(email=user_1.email, password=new_password)
    assert user.id == user_1.id


def test_invalid_uidb64_reset_password(client, user_1, user_1_reset_password_data):
    """Check if a reset password attempt with an invalid uidb64 returns a consistent error message"""
    _, token = user_1_reset_password_data
    invalid_uidb64 = "MmM3YWY5MGMtODAzMy00ZDY4LWJiOWEtOTdlZGIzN2ZkYzhj"
    new_password = "Valid Password"
    response = reset_password(
        client=client, uidb64=invalid_uidb64, token=token, password=new_password
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    user = authenticate(email=user_1.email, password=new_password)
    assert user is None


def test_invalid_token_reset_password(client, user_1, user_1_reset_password_data):
    """Check if a reset password attempt with an invalid token returns a consistent error message"""
    uidb64, _ = user_1_reset_password_data
    invalid_token = "wrong"
    new_password = "Valid Password"
    response = reset_password(
        client=client, uidb64=uidb64, token=invalid_token, password=new_password
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    user = authenticate(email=user_1.email, password=new_password)
    assert user is None


def test_successful_reset_password_with_a_trimmable_new_password(
    client,
    user_1,
    user_1_reset_password_data,
    format_response,
):
    """
    Check if when a user reset its password using a trimmable new password
    (starting or/and ending with a blank space) it is correctly stored in the database
    """
    uidb64, token = user_1_reset_password_data
    new_password = "Valid Trimmable Password "
    response = reset_password(
        client=client, uidb64=uidb64, token=token, password=new_password
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == format_response(
        ResetPasswordMessages.RESET_PASSWORD_SUCCESSFULLY.value
    )
    user = authenticate(email=user_1.email, password=new_password)
    assert user
    assert user.id == user_1.id
