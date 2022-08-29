from django.urls import path

# apps
from supplier import views

app_name = "supplier"

urlpatterns = [
    # supplier
    path(
        "supplier/<str:slug>",
        views.SupplierDetailView.as_view(),
        name="supplier-detail",
    ),
    # products
    path("products/", views.ProductListView.as_view(), name="products"),
    path(
        "products/<str:slug>", views.ProductDetailView.as_view(), name="product-detail"
    ),
    path("new-arivals/", views.NewArrivalView.as_view(), name="new-arivals"),
    # categories
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "category/<str:slug>",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    # subcategory
    path(
        "category/<str:category_slug>/subcategory/<str:sub_category_slug>",
        views.SubCategoryDetailView.as_view(),
        name="subcategory-detail",
    ),
    # store
    path(
        "store/<str:slug>",
        views.StoreDetailView.as_view(),
        name="store-detail",
    ),
    path(
        "stores",
        views.StoreListView.as_view(),
        name="store-list",
    ),
    # path("stores/", views.CategoryListView.as_view(), name="store-list"),
    # path(
    #     "category/<str:slug>",
    #     views.CategoryDetailView.as_view(),
    #     name="category-detail",
    # ),
    path(
        "search",
        views.SearchView.as_view(),
        name="search",
    ),
    # dashboard
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path(
        "dashboard/products",
        views.DashboardProductsView.as_view(),
        name="dashboard-products",
    ),
    path(
        "dashboard/productscreate",
        views.DashboardProductsCreateView.as_view(),
        name="dashboard-productscreate",
    ),
    path(
        "dashboard/stores", views.DashboardStoresView.as_view(), name="dashboard-stores"
    ),
    path(
        "dashboard/storescreate",
        views.DashboardStoresCreateView.as_view(),
        name="dashboard-storescreate",
    ),
    path(
        "dashboard/contracts",
        views.DashboardContractsView.as_view(),
        name="dashboard-contracts",
    ),
    path(
        "dashboard/contractsdetails/<int:pk>",
        views.DashboardContractsDetailsView.as_view(),
        name="dashboard-contractsdetails",
    ),
    path(
        "dashboard/services",
        views.DashboardServicesView.as_view(),
        name="dashboard-services",
    ),
    path(
        "dashboard/servicescreate",
        views.DashboardServicesCreateView.as_view(),
        name="dashboard-servicescreate",
    ),
]
