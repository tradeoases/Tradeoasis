from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q

from supplier import models as SupplierModels
from manager import models as ManagerModels


class ProductListView(ListView):
    model = SupplierModels.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sub_categories = SupplierModels.ProductSubCategory.objects.all()[:10]

        object_list = []
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
                                "image": SupplierModels.ProductImage.objects.filter(
                                    product=product
                                ).first(),
                            }
                            for product in sub_category.product_set.all()
                        ]
                    },
                }
                object_list.append(sub_category_group)

        context["object_list"] = object_list

        context["view_name"] = "Products"
        context["product_categories"] = {
            "context_name": "product-categories",
            "results": SupplierModels.ProductCategory.objects.all().order_by("-id"),
        }

        # deals, suggestion, new arrivals are to be added in context

        return context


class ProductDetailView(DetailView):
    model = SupplierModels.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context["view_name"] = product.name
        context["product_stores"] = {
            "context_name": "product-categories",
            "results": product.store.all(),
        }
        context["product_categories"] = {
            "context_name": "product-categories",
            "results": SupplierModels.ProductCategory.objects.all().order_by(
                "-created_on"
            ),
        }
        context["product_images"] = {
            "context_name": "product-images",
            "results": SupplierModels.ProductImage.objects.filter(product=product),
        }
        context["related_products"] = {
            "context_name": "related-product",
            "results": SupplierModels.Product.objects.filter(
                Q(sub_category=product.sub_category), ~Q(id=product.id)
            ),
        }
        return context


class CategoryListView(ListView):
    model = SupplierModels.ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = self.get_queryset()

        context["view_name"] = "Categories"

        object_list = []
        for category in categories:
            category_group = {
                "category": category,
                "sub_categories": SupplierModels.ProductSubCategory.objects.filter(
                    category=category
                ),
            }
            object_list.append(category_group)

        context["context_name"] = "product-categories"
        context["object_list"] = object_list

        return context


class CategoryDetailView(DetailView):
    model = SupplierModels.ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()

        context["view_name"] = category.name

        products = []
        for sub_category in SupplierModels.ProductSubCategory.objects.filter(
            category=category
        ):
            if not sub_category.product_set.count() < 1:
                sub_category_group = {
                    "sub_category": sub_category.name,
                    "count": sub_category.product_set.count(),
                    "results": {
                        "products": [
                            {
                                "product": product,
                                "image": SupplierModels.ProductImage.objects.filter(
                                    product=product
                                ).first(),
                            }
                            for product in sub_category.product_set.all()
                        ]
                    },
                }
                products.append(sub_category_group)

        context["products"] = {"context_name": "products", "results": products}

        context["product_count"] = {
            "context_name": "product-count",
            "results": category.product_count,
        }
        context["other_categories"] = {
            "context_name": "other-categories",
            "results": SupplierModels.ProductCategory.objects.all()[:20],
        }

        return context


class SubCategoryDetailView(View):
    model = SupplierModels.ProductSubCategory
    template_name = "supplier/products.html"

    def get(self, request, category_slug, sub_category_slug):

        return render(
            request,
            template_name=self.template_name,
            context=self.get_context_data(
                category_slug=category_slug, sub_category_slug=sub_category_slug
            ),
        )

    def get_context_data(self, *args, **kwargs):
        context_data = dict()

        subcategory = self.model.objects.filter(
            slug=kwargs.get("sub_category_slug")
        ).first()

        context_data["view_name"] = subcategory.name

        context_data["subcategory_data"] = {
            "context-name": "subcategory-data",
            "results": {
                "category": subcategory.category,
                "sub_category": subcategory,
                "count": subcategory.product_set.count(),
            },
        }

        context_data["products"] = {
            "context-name": "products",
            "results": [
                {"product": product, "image": product.productimage_set.all().first()}
                for product in SupplierModels.Product.objects.filter(
                    sub_category=subcategory
                )
            ],
        }

        context_data["related_subcategories"] = {
            "context-name": "related-subcategories",
            "results": self.model.objects.filter(
                Q(category=subcategory.category), ~Q(id=subcategory.id)
            ),
        }
        return context_data


class StoreDetailView(DetailView):
    model = SupplierModels.Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        store = self.get_object()

        context["view_name"] = store.name
        context["showrooms"] = {
            "context_name": "showrooms",
            "results": ManagerModels.Showroom.objects.filter(store=store),
        }
        context["products"] = {
            "context_name": "products",
            "results": SupplierModels.Product.objects.filter(store=store),
        }
        context["product_count"] = {
            "context_name": "product-count",
            "results": SupplierModels.Product.objects.filter(store=store).count(),
        }
        context["related_stores"] = {
            "context_name": "related-stores",
            "results": SupplierModels.Store.objects.filter(
                supplier=store.supplier
            ).order_by("-id")[:6],
        }
        return context
