import json

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from authentication.enums.codes import ErrorCodes
from authentication.enums.messages import AuthMessages


def signout(client, access_token=None, refresh_token=None):
    """
    Make a request to the signout endpoint
    Args:
        client: HTTP Client
        email: The email from the user that is trying to signin
        password: The password from the user that is trying to signin
    Returns: Signout endpoint response
    """
    return client.post(
        path=reverse("auth:signout"),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access_token}" if access_token else None,
        data=json.dumps({"refresh_token": refresh_token}),
    )


def test_view_is_restricted(client):
    """Test if the signout gives an consistent error message for unauthenticated users"""
    response = signout(client=client)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_signout_successfully(user_factory, make_refresh_token, client):
    """Test if the signout is successful for logged users"""
    user = user_factory()
    refresh_token = make_refresh_token(user)
    response = signout(
        client=client,
        access_token=str(refresh_token.access_token),
        refresh_token=str(refresh_token),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_signout_with_expired_token(user_factory, make_refresh_token, client):
    """Test if the signout gives a consistent error message for expired tokens"""
    user = user_factory()

    with freeze_time("2021-08-30 11:02:00"):
        refresh_token = make_refresh_token(user)

    with freeze_time("2021-08-31 17:30:00"):
        response = signout(
            client=client,
            access_token=str(refresh_token.access_token),
            refresh_token=str(refresh_token),
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "code": "token_not_valid",
        "detail": "Given token not valid for any token type",
        "messages": [
            {
                "message": "Token is invalid or expired",
                "token_class": "AccessToken",
                "token_type": "access",
            }
        ],
    }


def test_signout_with_token_already_in_blocklist(
    user_factory, make_refresh_token, client
):
    """Test if the signout gives a consistent error message for blocklisted tokens"""
    user = user_factory()
    refresh_token = make_refresh_token(user)

    refresh_token.blacklist()

    response = signout(
        client=client,
        access_token=str(refresh_token.access_token),
        refresh_token=str(refresh_token),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "code": ErrorCodes.TOKEN_NOT_VALID.value,
        "detail": AuthMessages.TOKEN_INVALID.value,
    }


def test_signout_with_empty_fields(client, user_factory, make_refresh_token):
    """Test if the signout error message for empty refresh token is consistent"""
    user = user_factory()
    refresh_token = make_refresh_token(user)

    response = signout(
        client=client,
        access_token=str(refresh_token.access_token),
        refresh_token="",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "refresh_token": ["This field may not be blank."],
    }
