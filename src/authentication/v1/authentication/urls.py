from django.urls import path

from .refresh.views import TokenRefreshView
from .signin.views import Signin
from .signout.views import Signout
from .signup.views import Signup

urls = [
    path("signup", Signup.as_view(), name="signup"),
    path("signin", Signin.as_view(), name="signin"),
    path("signout", Signout.as_view(), name="signout"),
    path("refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
