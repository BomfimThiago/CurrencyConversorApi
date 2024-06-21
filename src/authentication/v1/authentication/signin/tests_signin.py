import json

from django.urls import reverse
from rest_framework import status

from authentication.enums.messages import AuthMessages

PASSWORD = "123456"


def signin(client, email, password):
    """
    Make a request to the signin endpoint
    Args:
        client: HTTP Client
        email: The email from the user that is trying to signin
        password: The password from the user that is trying to signin
    Returns: Signin endpoint response
    """

    return client.post(
        path=reverse("auth:signin"),
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )


def test_signin_successfully(
    client,
    user_factory,
    make_refresh_token,
    mocker,
    format_response,
):
    """Check if a user signin with correct email and password is succesful"""
    user = user_factory.create(password="123456")
    refresh_token = make_refresh_token(user)

    mocker.patch(
        "authentication.utils.jwt.AccessToken",
        return_value=refresh_token.access_token,
    )
    mocker.patch(
        "authentication.utils.jwt.RefreshToken.for_user",
        return_value=refresh_token,
    )

    response = signin(client=client, email=user.email, password=PASSWORD)

    assert response.status_code == status.HTTP_200_OK

    data = {
        "access_token": str(refresh_token.access_token),
        "refresh_token": str(refresh_token),
    }
    assert response.json() == format_response(AuthMessages.LOGIN_SUCCESSFUL.value, data)


def test_signin_with_incorrect_format_email(client):
    """Check if the user signin with incorrect email format response is consistent"""
    response = signin(client=client, email="incorrect.format.email", password=PASSWORD)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"email": ["Enter a valid email address."]}


def test_signin_with_incorrect_email(client, user_factory):
    """Check if the signin with an incorrect email gives a consistent error message"""
    user_factory(password=PASSWORD)

    response = signin(
        client=client, email="incorrect.email@example.com", password=PASSWORD
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": AuthMessages.WRONG_CREDENTIALS.value}


def test_singin_with_incorrect_password(client, user_factory):
    """Check if the signin with an incorrect password gives a consistent error message"""
    user = user_factory()

    response = signin(client=client, email=user.email, password="incorrect_password")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": AuthMessages.WRONG_CREDENTIALS.value}


def test_singin_with_empty_fields(client):
    """Check if the signin with empty fields gives a consistent error message"""
    response = signin(client=client, email="", password="")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "email": ["This field may not be blank."],
        "password": ["This field may not be blank."],
    }


def test_signin_with_trimmable_password_correctly(
    client,
    user_factory,
    make_refresh_token,
    mocker,
    format_response,
):
    """Check if the signin with a trimmable password (starting or/and ending with a blank space) works correctly"""
    trimmable_password = f"{PASSWORD} "
    user = user_factory(password=trimmable_password)
    refresh_token = make_refresh_token(user)

    mocker.patch(
        "authentication.utils.jwt.AccessToken",
        return_value=refresh_token.access_token,
    )
    mocker.patch(
        "authentication.utils.jwt.RefreshToken.for_user",
        return_value=refresh_token,
    )

    response = signin(client=client, email=user.email, password=trimmable_password)

    assert response.status_code == status.HTTP_200_OK

    data = {
        "access_token": str(refresh_token.access_token),
        "refresh_token": str(refresh_token),
    }
    assert response.json() == format_response(AuthMessages.LOGIN_SUCCESSFUL.value, data)


def test_signin_into_an_account_with_trimmable_password_trimming_it_unsuccessfully(
    client, user_factory
):
    """
    Check if a user cannot signin on an account that has a trimmable password
    (starting or/and ending with a blank space) when passing the trimmed string to the endpoint
    """
    user = user_factory(password=f" {PASSWORD}")

    response = signin(client=client, email=user.email, password=PASSWORD)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": AuthMessages.WRONG_CREDENTIALS.value}
