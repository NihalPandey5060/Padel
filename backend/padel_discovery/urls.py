from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="Padel Discovery AI API", version="1.0.0")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("padel_discovery.core.urls")),
    path("api/schema/", schema_view, name="openapi-schema"),
]
