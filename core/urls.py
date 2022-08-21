from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext as _

urlpatterns = i18n_patterns(
    path("", include("manager.urls", namespace="manager")),
    path(_("suppliers/"), include("supplier.urls", namespace="supplier")),
    path(_("buyer/"), include("buyer.urls", namespace="buyer")),
    path(_("auth/"), include("auth_app.urls", namespace="auth")),
    path(_("support/admin/"), include("app_admin.urls", namespace="app_admin")),
    path(_("admin-api/"), include("admin_api.urls", namespace="admin-api")),
    path(_("admin/"), admin.site.urls),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
