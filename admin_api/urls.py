from django.urls import path

from admin_api import views

app_name = "admin_api"

urlpatterns = [
    path("suppliers/", views.SupplierListView.as_view(), name="suppliers-list"),
    path("supplier/<str:slug>", views.SupplierRetrieveView.as_view(), name="supplier"),

    path("buyers/", views.BuyersListView.as_view(), name="buyers-list"),
    path("buyer/<str:slug>", views.BuyerRetrieveView.as_view(), name="buyer"),

    path("products/", views.ProductsListView.as_view(), name="products-list"),
    path("product-images/<str:slug>", views.ProductImageListView.as_view(), name="product-images-list"),
    path("product/<str:slug>", views.ProductRetrieveView.as_view(), name="product"),
    path("products/supplier/<str:slug>", views.SupplierProductsListView.as_view(), name="supplier-product"),

    path("contracts/", views.ContractsListView.as_view(), name="contracts-list"),
    path("contract/<str:id>", views.ContractRetrieveView.as_view(), name="contract"),

    path("showrooms/", views.ShowroowListView.as_view(), name="showroow-list"),
    path('showrooms/<str:slug>', views.ShowroowRetrieveView.as_view(), name='store'),
    path('showrooms/supplier/<str:slug>', views.SupplierShowroowListView.as_view(), name='supplier-showroow-list'),

    path("manager-services/", views.ManagerServicesListView.as_view(), name="manager-services-list"),
    path("manager-service/<str:slug>", views.ManagerServiceRetrieveView.as_view(), name="manager-service"),

    path("memberships/", views.MembershipListView.as_view(), name="membership-list"),

    path('stores/', views.StoreListView.as_view(), name='store-list'),
    path('stores/<str:slug>', views.StoreRetrieveView.as_view(), name='store'),
    path('stores/supplier/<str:slug>', views.SupplierStoresListView.as_view(), name='supplier-store-list'),

    path("services/", views.ServicesListView.as_view(), name="services-list"),
    path("service/<str:slug>", views.ServiceRetrieveView.as_view(), name="service"),

]
