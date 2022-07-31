from nis import cat
from typing import List
from unicodedata import category
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q

# apps
from supplier.models import Product, ProductCategory, Store, ProductImage
from manager.models import Showroom


class HomeView(View):
    template_name = "manager/home.html"

    def get(self, request):
        # generating products context
        categories = ProductCategory.objects.all()[:10]
        product_object_list = []
        for category in categories:
            if not category.product_set.count() < 1:
                category_group = {
                    "category": category.name,
                    "count": category.product_set.count(),
                    "results": {
                        "products" : [
                            {
                                "product": product,
                                "image": ProductImage.objects.filter(product=product).first()
                            }
                        for product in category.product_set.all()]
                    },
                }
                product_object_list.append(category_group)

        context_data = {
            "view_name": "Home",
            "product_categories": {
                "context_name": "product-categories",
                "results": ProductCategory.objects.all().order_by("-created_on"),
            },
            "showrooms": {
                "context_name": "showrooms",
                "results": Showroom.objects.all().order_by('-id')[:6],
            },
            "stores": {"context_name": "stores", "results": Store.objects.all().order_by('-id')[:6]},

            "catogory_product_group": {
                "context_name": "catogory-product-group",
                "results": product_object_list
            },

            "new_arrivals": {
                "context_name": "new-arrivals",
                "results": Product.objects.all().order_by('-id')[:6],
            },
        }
        return render(request, self.template_name, context=context_data)


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = ProductCategory.objects.all()

        object_list = []
        for category in categories:
            if not category.product_set.count() < 1:
                category_group = {
                    "category": category.name,
                    "count": category.product_set.count(),
                    "results": {
                        "products" : [
                            {
                                "product": product,
                                "image": ProductImage.objects.filter(product=product).first()
                            }
                        for product in category.product_set.all()]
                    },
                }
                object_list.append(category_group)

        context['object_list'] = object_list

        context["view_name"] = "Product"
        context["product_categories"] = {
            "context_name": "product-categories",
            "results": ProductCategory.objects.all().order_by("-id"),
        }

        # deals, suggestion, new arrivals are to be added in context

        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context["view_name"] = product.name
        context["product_storess"] = {
            "context_name": "product-categories",
            "results": product.store.all(),
        }
        context["product_categories"] = {
            "context_name": "product-categories",
            "results": ProductCategory.objects.all().order_by("-created_on"),
        }
        context["product_images"] = {
            "context_name": "product-images",
            "results": ProductImage.objects.filter(product=product),
        }
        context["related_products"] = {
            "context_name": "related-product",
            "results": Product.objects.filter(
                Q(category=product.category), ~Q(id=product.id)
            ),
        }
        return context


class CategoryListView(ListView):
    model = ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Categories"
        return context

class CategoryDetailView(DetailView):
    model = ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()

        context["view_name"] = category.name
        context["products"] = {
            "context_name": "products",
            "results": category.product_set.all()
        }
        context["product_count"] = {
            "context_name": "product-count",
            "results": category.product_set.count()
        }
        context["other_categories"] = {
            "context_name": "other-categories",
            "results": ProductCategory.objects.all()[:20],
        }

        return context