from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("landlords.urls")),
    path("api/", include("accommodations.urls")),
    path("api/", include("reviews.urls")),
    path("api/intelligence/", include("intelligence.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)