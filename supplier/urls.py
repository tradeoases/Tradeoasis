from django.urls import path

# apps
from supplier import views

app_name = "supplier"

urlpatterns = [
    # supplier
    path(
        "supplier/<str:slug>", views.SupplierDetailView.as_view(), name="supplier-detail"
    ),

    # products
    path("products/", views.ProductListView.as_view(), name="products"),
    path(
        "products/<str:slug>", views.ProductDetailView.as_view(), name="product-detail"
    ),
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
    )
    # path("stores/", views.CategoryListView.as_view(), name="store-list"),
    # path(
    #     "category/<str:slug>",
    #     views.CategoryDetailView.as_view(),
    #     name="category-detail",
    # ),
]
