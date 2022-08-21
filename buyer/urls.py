from django.urls import path

app_name = "buyer"

from buyer import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("contracts/", views.ContractListView.as_view(), name="contracts"),
    path("product/", views.VisitedProductsListView.as_view(), name="products"),
]
