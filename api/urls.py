from django.urls import path

app_name = "api"

from api import views

urlpatterns = [
    path("stores/", views.StoresListView.as_view(), name="stores"),
    path("products/", views.ProductsListView.as_view(), name="products"),
    path(
        "loading_products/",
        views.LoadingProductsListView.as_view(),
        name="loading_products",
    ),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),
    path("services/", views.ServicesListView.as_view(), name="services"),
]
