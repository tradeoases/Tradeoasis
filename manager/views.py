from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
import random
from django.utils.translation import gettext as _

# apps
from supplier.models import (
    Product,
    ProductCategory,
    Store,
    ProductImage,
    ProductSubCategory,
)
from manager import models as ManagerModels


class HomeView(View):
    template_name = "manager/index.html"

    def get(self, request):
        # generating products context
        sub_categories = ProductSubCategory.objects.all()[:10]
        product_object_list = []
        for sub_category in sub_categories:
            if not sub_category.product_set.count() < 1:
                sub_category_group = {
                    "sub_category": sub_category.name,
                    "category": sub_category.category.name,
                    "count": sub_category.category.product_count,
                    "results": {
                        "products": [
                            {
                                "product": product,
                                "image": ProductImage.objects.filter(
                                    product=product
                                ).first(),
                            }
                            for product in sub_category.product_set.all()
                        ]
                    },
                }
                product_object_list.append(sub_category_group)

        context_data = {
            "view_name": _("Home"),
            "product_categories": {
                "context_name": "product-categories",
                "results": [
                    {
                        "category": category,
                        "sub_categories": ProductSubCategory.objects.filter(
                            category=category
                        ),
                    }
                    for category in ProductCategory.objects.all().order_by(
                        "-created_on"
                    )[:6]
                    if category.product_count > 0
                    and category.productsubcategory_set.count()
                ],
            },
            "showrooms": {
                "context_name": "showrooms",
                "results": ManagerModels.Showroom.objects.all().order_by("-id")[:6],
            },
            "catogory_product_group": {
                "context_name": "catogory-product-group",
                "results": product_object_list,
            },
            "new_arrivals": {
                "context_name": "new-arrivals",
                "results": [
                    {
                        "product": product,
                        "main_image": ProductImage.objects.filter(
                            product=product
                        ).first(),
                    }
                    for product in (
                        lambda products: random.sample(products, len(products))
                    )(list(Product.objects.all().order_by("-id")[:10]))
                ],
            },
            "discounts": {
                "context_name": "discounts",
                "results": [
                    {
                        "product": product,
                        "main_image": ProductImage.objects.filter(
                            product=product
                        ).first(),
                        "sub_images": ProductImage.objects.filter(product=product)[1:4],
                    }
                    for product in Product.objects.all().order_by("-id")[:6]
                ],
            },
            "propular_products": {
                "context_name": "propular-products",
                "results": [
                    {
                        "product": product,
                        "supplier": product.store.all().first().supplier,
                        "images": ProductImage.objects.filter(product=product).first(),
                    }
                    for product in Product.objects.all().order_by("-id")[:12]
                ],
            },
        }
        return render(request, self.template_name, context=context_data)


# showrooms
class ShowRoomListView(ListView):
    model = ManagerModels.Showroom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["view_name"] = _("Showrooms")
        context["object_list"] = {
            "context_name": "showrooms",
            "results": [
                {"showroom": showroom, "store_count": showroom.store.count()}
                for showroom in (
                    lambda showrooms: random.sample(showrooms, len(showrooms))
                )(list(ManagerModels.Showroom.objects.all()[:20]))
            ],
        }
        context["stores"] = {
            "context_name": "stores",
            "results": (lambda stores: random.sample(stores, len(stores)))(
                list(Store.objects.all()[:10])
            ),
        }
        return context


class ShowRoomDetailView(DetailView):
    model = ManagerModels.Showroom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        showroom = self.get_object()

        context["view_name"] = showroom.name
        context["stores"] = {"context_name": "stores", "results": showroom.store.all()}
        context["other_showroom"] = {
            "context_name": "other-showroom",
            "results": [
                {"showroom": showroom, "store_count": showroom.store.count()}
                for showroom in (
                    lambda showrooms: random.sample(showrooms, len(showrooms))
                )(list(ManagerModels.Showroom.objects.all()[:10]))
            ],
        }
        context["products"] = {
            "context_name": "products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in (
                    lambda products: random.sample(products, len(products))
                )(
                    [
                        product
                        for product in Product.objects.filter(
                            store__in=showroom.store.all()
                        )
                    ][:20]
                )
            ],
        }

        return context


class ServiceListView(ListView):
    model = ManagerModels.Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["view_name"] = _("Services")
        return context


class AboutUsView(TemplateView):
    template_name = "manager/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["view_name"] = _("About Us")
        return context


def profile(request):
    if not request.user.is_authenticated:
        return redirect(
            "{}?next={}".format(reverse("auth_app:login"), request.GET.get("next"))
        )

    if request.user.account_type == "SUPPLIER":
        # to supplier profile
        return redirect(reverse("manager:home"))
    elif request.user.account_type == "BUYER":
        # to buyer profile
        return redirect(reverse("buyer:profile"))
    elif request.user.account_type == "SUPPORT": 
        return redirect(reverse("app_admin:profile"))
    elif request.user.is_superuser:
        return redirect(reverse("app_admin:profile"))
        

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(
            "{}?next={}".format(reverse("auth_app:login"), request.GET.get("next"))
        )

    if request.user.account_type == "SUPPLIER":
        # to supplier dashboard
        return redirect(reverse("manager:home"))
    elif request.user.account_type == "BUYER":
        # to buyer dashboard
        return redirect(reverse("buyer:profile"))
    elif request.user.account_type == "SUPPORT":
        return redirect(reverse("app_admin:home"))
    elif request.user.is_superuser:
        return redirect(reverse("app_admin:home"))
