from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from authentication import urls as auth_urls
from core.views import health_check
from transactions import urls as transactions_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    # Enables the DRF browsable API page
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("health_check/", health_check, name="health_check"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("auth/", include(auth_urls)),
    path("transactions/", include(transactions_urls)),
]

if settings.ENVIRONMENT == "development":
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
