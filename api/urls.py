from django.urls import path

app_name = "api"

from api import views

urlpatterns = [
    path("stores/", views.StoresListView.as_view(), name="stores"),
    path(
        "supplier/contracts/",
        views.SupplierContractsListView.as_view(),
        name="supplier/contracts",
    ),
    path("services/", views.ServicesListView.as_view(), name="services"),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),


    #---------------------------------------- Products ----------------------------------------
    path("products/", views.ProductsListView.as_view(), name="products"),
    path("supplier/products/", views.SupplierProductsListView.as_view(), name="supplier-products"),
    path("supplier/products/create/", views.ProductCreateApiView.as_view(), name="supplier-product-create"),
    path("supplier/products/<str:slug>/create/<str:data_type>/", views.ProductAppendDetailsApiView.as_view(), name="supplier-product-append-details"),
    path(
        "loading_products/",
        views.LoadingProductsListView.as_view(),
        name="loading_products",
    ),
    #---------------------------------------- Products ----------------------------------------

    #---------------------------------------- Calender ----------------------------------------
    path("events/", views.CalenderEventListView.as_view(), name="events"),
    path("events/create/", views.CalenderEventCreateView.as_view(), name="event-create"),
    path("events/<int:pk>/details/", views.CalenderEventDetailView.as_view(), name="event-detail"),
    path("events/<int:pk>/delete/", views.CalenderEventDeleteView.as_view(), name="event-detail"),
    #---------------------------------------- Calender ----------------------------------------


    #---------------------------------------- Cart ----------------------------------------
    path("cart/", views.CartListView.as_view(), name="cart"),
    path("cart/product/<str:product_slug>/add/", views.CartAppeendAppendView.as_view(), name="cart-add-product"),
    path("cart/product/<str:product_slug>/delete/", views.CartDeleteProductView.as_view(), name="wishlist-delete-product"),
]
