from django.urls import include, path

from .authentication.urls import urls as authentication_urls
from .reset_password.urls import urls as reset_password_urls
from .terms.urls import urls as terms_urls

urls = [
    path("", include(authentication_urls)),
    path("", include(reset_password_urls)),
    path("", include(terms_urls)),
]
