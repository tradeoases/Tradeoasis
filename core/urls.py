from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext as _

# from django.core.signals import request_finished, got_request_exception
# from django.dispatch import receiver
# from manager.models import UserRequest
# # from django.contrib.gis.geoip2 import GeoIP2
# # g = GeoIP2()

# @receiver(request_finished)
# def requestTracker(request, sender, **kwargs):
    # if request.user_agent.is_mobile:
    #     user_device = "mobile"
    # elif request.user_agent.is_tablet:
    #     user_device = "tablet"
    # elif request.user_agent.is_bot:
    #     user_device = "bot"
    # else:
    #     user_device = "pc"

    # user_os = request.user_agent.os.family
    # view  = request.resolver_match.url_name
    # request_method = request.method

    # ip = request.META.get('REMOTE_ADDR', None)
    # if ip:
    #     city = g.city(ip)['city']
    #     city = g.country(ip)['city']
    # else:
    #     city = 'Undefined' # default city


    # print("*"*50)
    # print("Request finished!")
    # print("*"*50)
    # pass


# @receiver(got_request_exception)
# def get_exception_response(request, resolver, status_code, exception, sender=None):
    # try:
    #     callback, param_dict = resolver.resolve_error_handler(status_code)
    #     response = callback(request, **dict(param_dict, exception=exception))
    # except Exception:
    #     signals.got_request_exception.send(sender=sender, request=request)
    #     response = handle_uncaught_exception(request, resolver, sys.exc_info())

    # return response
    # pass


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

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
