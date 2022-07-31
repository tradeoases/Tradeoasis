from django.urls import path

# apps
from manager import views

app_name = "manager"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # products
    path("products/", views.ProductListView.as_view(), name="products"),
    path(
        "products/<str:slug>", views.ProductDetailView.as_view(), name="product-detail"
    ),

    # categories
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "category/<str:slug>", views.CategoryDetailView.as_view(), name="category-detail"
    ),



    path("showrooms/", views.HomeView.as_view(), name="showrooms"),
    path("services/", views.HomeView.as_view(), name="services"),
    path("support/", views.HomeView.as_view(), name="support"),
    path("about-us/", views.HomeView.as_view(), name="about-us"),
]
