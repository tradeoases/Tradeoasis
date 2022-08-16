from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("manager.urls", namespace="manager")),
    path("suppliers/", include("supplier.urls", namespace="supplier")),
    path("support/admin/", include("app_admin.urls", namespace="app_admin")),
    path("admin-api/", include("admin_api.urls", namespace="admin-api")),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
