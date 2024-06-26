import json

from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

ID = 1
EMAIL = "john.doe@example.com"
PASSWORD = "123456"
FULL_NAME = "John Doe"


def signup(client, **user_data):
    """
    Make a request to the signup endpoint
    Args:
        client: HTTP Client
        user_data: The data that will be used for the user's registration
    Returns: Signin endpoint response
    """
    return client.post(
        path=reverse("auth:signup"),
        data=json.dumps(user_data),
        content_type="application/json",
    )


def test_signup_successfully(client, db):
    """Check if the signup with valid data is successful"""
    response = signup(
        client=client,
        email=EMAIL,
        password=PASSWORD,
        full_name=FULL_NAME,
    )

    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data["data"]["user"]["email"] == EMAIL
    assert response_data["data"]["user"]["full_name"] == FULL_NAME


def test_signup_with_empty_request_body(client):
    """Check if the signup with empty data gives a consistent error message"""
    response = signup(client=client)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "full_name": ["This field is required."],
        "email": ["This field is required."],
        "password": ["This field is required."],
    }


def test_signup_with_email_that_has_invalid_format(client, db):
    """Check if the signup with invalid format email gives a consistent error message"""
    response = signup(
        client=client,
        email="email.with.invalid.format",
        password=PASSWORD,
        full_name=FULL_NAME,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "email": ["Enter a valid email address."],
    }


def test_signup_with_email_already_registered(user_factory, client):
    """Check if the signup with an email already registered returns a consistent error message"""
    user_factory(email=EMAIL)

    response = signup(
        client=client,
        email=EMAIL,
        password=PASSWORD,
        full_name=FULL_NAME,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"email": ["This field must be unique."]}


def test_signup_with_trimmable_password(client, db) -> None:
    """
    Check if the signup with a trimmable password (starting or/and ending with a blank space)
    creates the hash for the full string with the space
    """
    password = f" {PASSWORD} "
    response = signup(
        client=client,
        email=EMAIL,
        password=password,
        full_name=FULL_NAME,
    )

    assert response.status_code == status.HTTP_201_CREATED

    created_user = authenticate(email=EMAIL, password=password)
    assert created_user
    assert created_user.id == created_user.id
