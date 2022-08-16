from django.urls import path

from admin_api import views

app_name = "admin_api"

urlpatterns = [
    path("suppliers/", views.SupplierListView.as_view(), name="suppliers-list"),
    path("supplier/<str:slug>", views.SupplierRetrieveView.as_view(), name="supplier"),

    path("buyers/", views.BuyersListView.as_view(), name="buyers-list"),
    path("buyer/<str:slug>", views.BuyerRetrieveView.as_view(), name="buyer"),

    path("products/", views.ProductsListView.as_view(), name="products-list"),
    path("product/<str:slug>", views.ProductRetrieveView.as_view(), name="product"),
    path("products/supplier/<str:slug>", views.SupplierProductsListView.as_view(), name="supplier-product"),

    path("contracts/", views.ContractsListView.as_view(), name="contracts-list"),
    path("contract/<str:slug>", views.ContractRetrieveView.as_view(), name="contract"),

    path("showroow/", views.ShowroowListView.as_view(), name="showroow-list"),

    path("manager-services/", views.ManagerServicesListView.as_view(), name="manager-services-list"),
    path("manager-service/<str:slug>", views.ManagerServiceRetrieveView.as_view(), name="manager-service"),

    path("membership/", views.MembershipListView.as_view(), name="membership-list"),
]
