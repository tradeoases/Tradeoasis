from django.urls import path
from app_admin import views

app_name = "app_admin"

urlpatterns = [
    path("", views.AdminDashboardView.as_view(), name="home"),
    path("clients/", views.AdminClientsView.as_view(), name="clients"),
    # manager
    path("manager/", views.AdminManagersView.as_view(), name="manager"),
    path("manager/service", views.ServiceCreateView.as_view(), name="service-create"),
    path(
        "manager/showroom", views.ShowroomCreateView.as_view(), name="showroom-create"
    ),
    path(
        "manager/category", views.CategoryCreateView.as_view(), name="category-create"
    ),
    # support
    path("discussions/", views.AdminDiscussionsView.as_view(), name="discussions"),
    path("discussions/chat", views.AdminChatView.as_view(), name="discussion"),
    path("community/", views.AdminCommunityView.as_view(), name="community"),
    path(
        "community/chat", views.AdminCommunityChatView.as_view(), name="community-chat"
    ),
]
