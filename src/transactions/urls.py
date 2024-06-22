from django.urls import include, path

from .v1.urls import urls

app_name = "transactions"
urlpatterns = [path("v1/", include(urls))]
