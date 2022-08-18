from django.urls import path

# apps
from manager import views

app_name = "manager"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # showrooms
    path("showrooms/", views.ShowRoomListView.as_view(), name="showrooms"),
    path(
        "showroom/<str:slug>",
        views.ShowRoomDetailView.as_view(),
        name="showroom-detail",
    ),
    # services
    path("services/", views.ServiceListView.as_view(), name="services"),
    path("support/", views.HomeView.as_view(), name="support"),
    path("about/", views.AboutUsView.as_view(), name="about-us"),
    path("profile/", views.profile, name="profile"),
]
