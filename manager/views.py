from unicodedata import category
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q

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
            "view_name": "Home",
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
                    )[:7]
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
                "results": Product.objects.all().order_by("-id")[:6],
            },
            "weekly_deals": {
                "context_name": "weekly-deals",
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

        context["view_name"] = "Showrooms"
        context["locations"] = {
            "context_name": "locations",
            "results": ManagerModels.Location.objects.all(),
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
            "results": ManagerModels.Showroom.objects.all().order_by("-id")[:6],
        }
        return context
