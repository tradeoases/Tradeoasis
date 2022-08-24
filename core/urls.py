from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext as _

urlpatterns = i18n_patterns(
    path("", include("manager.urls", namespace="manager")),
    path(_("suppliers/"), include("supplier.urls", namespace="supplier")),
    path(_("buyer/"), include("buyer.urls", namespace="buyer")),
    path(_("auth/"), include("auth_app.urls", namespace="auth")),
    path(_("payments/"), include("payment.urls", namespace="payments")),
    path(_("support/admin/"), include("app_admin.urls", namespace="app_admin")),
    path(_("api/"), include("api.urls", namespace="api")),
    path(_("admin-api/"), include("admin_api.urls", namespace="admin-api")),
    path(_("admin/"), admin.site.urls),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
