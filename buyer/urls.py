from django.urls import path

app_name = "buyer"

from buyer import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("password-reset", views.password_reset, name="password-reset"),
    path(
        "editaccountsprofile/",
        views.EditAccountsProfileView.as_view(),
        name="dashboard-editaccountsprofile",
    ),
    path("business/", views.BusinessProfileView.as_view(), name="business"),
    path(
        "editbusinessprofile/<str:slug>/",
        views.EditBusinessProfileView.as_view(),
        name="dashboard-editbusinessprofile",
    ),
    path("contracts/", views.ContractListView.as_view(), name="contracts"),
    path("wishlist/", views.WishListView.as_view(), name="wishlist"),
    path("request-for-quote/", views.RequestForQuoteView.as_view(), name="request-for-quote"),
    path("order-tracking/", views.OrderTrackingView.as_view(), name="order-tracking"),
    path("order-history/", views.OrderHistoryView.as_view(), name="order-history"),
    path("messenger/", views.MessengerView.as_view(), name="messenger"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("notifications/", views.NotificationsView.as_view(), name="notifications"),
    path(
        "dashboard/contractsdetails/<int:pk>",
        views.DashboardContractsDetailsView.as_view(),
        name="dashboard-contractsdetails",
    ),
    path("product/", views.VisitedProductsListView.as_view(), name="products"),
]
