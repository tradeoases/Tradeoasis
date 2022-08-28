from django.urls import path

app_name = "buyer"

from buyer import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("business/", views.BusinessProfileView.as_view(), name="business"),
    path("contracts/", views.ContractListView.as_view(), name="contracts"),
    path(
        "dashboard/contractsdetails/<int:pk>",
        views.DashboardContractsDetailsView.as_view(),
        name="dashboard-contractsdetails",
    ),
    path("product/", views.VisitedProductsListView.as_view(), name="products"),
]
