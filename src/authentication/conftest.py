from typing import Callable

import factory
import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authentication.utils.jwt import AccessToken, RefreshToken
from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    full_name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs["password"] = make_password(kwargs["password"])
        return super(UserFactory, cls)._create(model_class, *args, **kwargs)


@pytest.fixture
def user_factory(db):
    return UserFactory


@pytest.fixture()
def make_refresh_token() -> Callable:
    def _make_refresh_token(user: User) -> RefreshToken:
        return RefreshToken.for_user(user)

    return _make_refresh_token


@pytest.fixture()
def make_access_token() -> Callable:
    def _make_access_token(user: User) -> AccessToken:
        return AccessToken.for_user(user)

    return _make_access_token


@pytest.fixture
def user_1(user_factory: Callable) -> User:
    return user_factory()


@pytest.fixture
def user_1_token(user_1: User) -> AccessToken:
    return AccessToken.for_user(user_1)


@pytest.fixture
def user_1_reset_password_data(user_1: User):
    uidb64 = urlsafe_base64_encode(force_bytes(user_1.pk))
    token = default_token_generator.make_token(user_1)
    return uidb64, token


@pytest.fixture()
def format_response() -> Callable:
    def _format_response(message, data=None):
        response = {"message": message}

        if data:
            response["data"] = data

        return response

    return _format_response
