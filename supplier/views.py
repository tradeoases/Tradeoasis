from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.contrib import messages

import random

from supplier import models as SupplierModels
from auth_app import models as AuthModels
from manager import models as ManagerModels
from payment import models as PaymentModels

from supplier.mixins import SupplierOnlyAccessMixin

from django.utils.translation import get_language
from googletrans import Translator
from django.conf import settings

translator = Translator()


class SupplierDetailView(DetailView):
    model = AuthModels.ClientProfile
    template_name = "supplier/supplier_detail.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        supplier = self.get_object()

        context["view_name"] = supplier.business_name

        context["supplier_service"] = {
            "context_name": "supplier-service",
            "results": SupplierModels.Service.objects.filter(supplier=supplier.user),
        }

        context["products"] = {
            "context-name": "products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in SupplierModels.Product.objects.all()
                if supplier.user in [store.supplier for store in product.store.all()]
            ],
        }
        context["related_stores"] = {
            "context_name": "related-stores",
            "results": SupplierModels.Store.objects.filter(Q(supplier=supplier.user))[
                :10
            ],
        }

        return context


class ProductListView(View):
    model = SupplierModels.ProductSubCategory
    template_name = "supplier/product_list.html"
    PER_PAGE_COUNT = 20

    def get(self, request):

        return render(
            request, template_name=self.template_name, context=self.get_context_data()
        )

    def get_queryset(self):

        # get query parameters
        min_price = self.request.GET.get("min-price", 0)
        max_price = self.request.GET.get("max-price", None)
        supplier = self.request.GET.get("supplier", "All")
        search = self.request.GET.get("search", None)

        if max_price and supplier != "All":
            return SupplierModels.Product.objects.filter(
                Q(price__gte=float(min_price) if min_price else float(0)),
                Q(price__lte=float(max_price)),
                Q(
                    store__supplier=AuthModels.Supplier.supplier.filter(
                        clientprofile__business_name=supplier
                    ).first()
                ),
            )

        elif max_price:
            return SupplierModels.Product.objects.filter(
                Q(price__gte=float(min_price) if min_price else float(0)),
                Q(price__lte=float(max_price)),
            )

        elif supplier != "All":
            return SupplierModels.Product.objects.filter(
                Q(price__gte=float(min_price) if min_price else float(0)),
                Q(
                    store__supplier=AuthModels.Supplier.supplier.filter(
                        clientprofile__business_name=supplier
                    ).first()
                ),
            )

        elif search:
            # we are searching for products based on name, sub category, category
            return SupplierModels.Product.objects.filter(
                Q(name__icontains=search)
                | Q(sub_category__name__icontains=search)
                | Q(category__name__icontains=search)
            )

        return SupplierModels.Product.objects.filter(
            price__gte=float(min_price) if min_price else float(0)
        )

    def get_products_paginator(self):

        queryset = self.get_queryset()

        self.products = random.sample(
            list(queryset.order_by("-id")),
            self.PER_PAGE_COUNT if queryset.count() >= 20 else queryset.count(),
        )

        paginator = Paginator(self.products, self.PER_PAGE_COUNT)

        page_num = self.request.GET.get("page", 1)
        return paginator.page(page_num)

    def get_context_data(self, **kwargs):
        context_data = dict()

        products_paginator = self.get_products_paginator()

        context_data["view_name"] = _("Products")
        context_data["page_obj"] = products_paginator
        context_data["product_count"] = len(self.products)
        context_data["current_page_number"] = self.request.GET.get("page", 1)

        context_data["products"] = {
            "context-name": "products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in products_paginator.object_list
            ],
        }

        context_data["new_arrivals"] = {
            "context_name": "new_arrivals",
            "results": [
                {
                    "product": product,
                    "main_image": SupplierModels.ProductImage.objects.filter(
                        product=product
                    ).first(),
                }
                for product in (
                    lambda products: random.sample(products, len(products))
                )(list(SupplierModels.Product.objects.all().order_by("-id")[:10]))
            ],
        }

        context_data["suppliers"] = {
            "context_name": "suppliers",
            "results": AuthModels.Supplier.supplier.all(),
        }

        context_data["price_limits"] = {
            "context_name": "price-limits",
            "results": {
                "min_price": self.request.GET.get("min-price", 0),
                "max_price": self.request.GET.get("max-price", None),
            },
        }

        context_data["supplier_filter"] = {
            "context_name": "supplier-filter",
            "results": self.request.GET.get("supplier", 0),
        }

        return context_data


class ProductDetailView(DetailView):
    model = SupplierModels.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context["view_name"] = product.name
        context["product_supplier"] = {
            "context_name": "product-supplier",
            "results": product.store.all().first().supplier,
        }
        context["product_stores"] = {
            "context_name": "product-stores",
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
        context["tags"] = SupplierModels.ProductTag.objects.filter(product=product)
        context["related_products"] = {
            "context_name": "related-products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": SupplierModels.ProductImage.objects.filter(
                        product=product
                    ).first(),
                }
                for product in (
                    lambda products: random.sample(products, len(products))
                )(
                    list(
                        SupplierModels.Product.objects.filter(
                            ~Q(id=product.id),
                            Q(sub_category=product.sub_category)
                            | Q(category=product.category),
                        )[:10]
                    )
                )
            ],
        }
        return context


class NewArrivalView(View):
    template_name = 'supplier/promotions.html'

    def get(self, request):

        return render(request, self.template_name, context=self.get_context_data())

    def get_queryset(self):
        return SupplierModels.Product.objects.all().order_by('-id')

    def get_products_paginator(self):

        PER_PAGE_COUNT = 20

        self.subcategory_products = self.get_queryset()

        paginator = Paginator(self.subcategory_products.order_by("-id"), PER_PAGE_COUNT)

        page_num = self.request.GET.get("page", 1)
        return paginator.page(page_num)

    def get_context_data(self, **kwargs):
        context_data = dict()

        products_paginator = self.get_products_paginator()
        context_data = dict()

        context_data['view_name'] = 'Promotions'
        context_data["page_obj"] = products_paginator
        context_data["product_count"] = self.subcategory_products.count()
        context_data["current_page_number"] = self.request.GET.get("page", 1)

        context_data['products'] = {
            "context_name" : "new_arrivals",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in products_paginator.object_list
            ],
        }

        # preview_products only show for suppliers with highest plan
        context_data['preview_products'] = {
            "context_name" : "preview_products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in products_paginator.object_list
            ],
        }

        return context_data

class CategoryListView(ListView):
    model = SupplierModels.ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = self.get_queryset()

        context["view_name"] = _("Categories")

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

        # products = []
        # for sub_category in SupplierModels.ProductSubCategory.objects.filter(
        #     category=category
        # ):
        #     if not sub_category.product_set.count() < 1:
        #         sub_category_group = {
        #             "sub_category": sub_category.name,
        #             "count": sub_category.product_set.count(),
        #             "results": {
        #                 "products": [
        #                     {
        #                         "product": product,
        #                         "image": SupplierModels.ProductImage.objects.filter(
        #                             product=product
        #                         ).first(),
        #                     }
        #                     for product in sub_category.product_set.all()
        #                 ]
        #             },
        #         }
        #         products.append(sub_category_group)

        context["products"] = {
            "context_name": "products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": SupplierModels.ProductImage.objects.filter(
                        product=product
                    ).first(),
                }
                for product in SupplierModels.Product.objects.filter(
                    sub_category__in=SupplierModels.ProductSubCategory.objects.filter(
                        category=category
                    )
                )
            ],
        }

        context["sub_categories"] = {
            "context_name": "sub-catogeries",
            "results": SupplierModels.ProductSubCategory.objects.filter(
                category=category
            ),
        }

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

    def get_queryset(self, subcategory):

        # get query parameters
        min_price = self.request.GET.get("min-price", 0)
        max_price = self.request.GET.get("max-price", None)
        supplier = self.request.GET.get("supplier", "All")

        if max_price and supplier != "All":
            return SupplierModels.Product.objects.filter(
                Q(sub_category=subcategory),
                Q(price__gte=float(min_price) if min_price else float(0)),
                Q(price__lte=float(max_price)),
                Q(
                    store__supplier=AuthModels.Supplier.supplier.filter(
                        clientprofile__business_name=supplier
                    ).first()
                ),
            )

        elif max_price:
            return SupplierModels.Product.objects.filter(
                Q(sub_category=subcategory),
                Q(price__gte=float(min_price) if min_price else float(0)),
                Q(price__lte=float(max_price)),
            )

        elif supplier != "All":
            return SupplierModels.Product.objects.filter(
                Q(sub_category=subcategory),
                Q(price__gte=float(min_price) if min_price else float(0)),
                Q(
                    store__supplier=AuthModels.Supplier.supplier.filter(
                        clientprofile__business_name=supplier
                    ).first()
                ),
            )

        return SupplierModels.Product.objects.filter(
            Q(sub_category=subcategory),
            Q(price__gte=float(min_price) if min_price else float(0)),
        )

    def get_products_paginator(self, subcategory):

        PER_PAGE_COUNT = 20

        self.subcategory_products = self.get_queryset(subcategory)

        paginator = Paginator(self.subcategory_products.order_by("-id"), PER_PAGE_COUNT)

        page_num = self.request.GET.get("page", 1)
        return paginator.page(page_num)

    def get_context_data(self, **kwargs):
        context_data = dict()

        self.subcategory = self.model.objects.filter(
            slug=kwargs.get("sub_category_slug")
        ).first()

        products_paginator = self.get_products_paginator(self.subcategory)

        context_data["view_name"] = self.subcategory.name
        context_data["page_obj"] = products_paginator
        context_data["product_count"] = self.subcategory_products.count()
        context_data["current_page_number"] = self.request.GET.get("page", 1)

        context_data["subcategory_data"] = {
            "context-name": "subcategory-data",
            "results": {
                "category": self.subcategory.category,
                "sub_category": self.subcategory,
                "count": self.subcategory.product_set.count(),
            },
        }

        context_data["products"] = {
            "context-name": "products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in products_paginator.object_list
            ],
        }

        context_data["discounts"] = {
            "context_name": "discounts",
            "results": [
                {
                    "product": product,
                    "main_image": SupplierModels.ProductImage.objects.filter(
                        product=product
                    ).first(),
                }
                for product in SupplierModels.Product.objects.all().order_by("-id")[:6]
            ],
        }

        context_data["related_subcategories"] = {
            "context_name": "related-subcategories",
            "results": [
                {
                    "subcategory": subcategory,
                    "products": [
                        {
                            "product": product,
                            "main_image": SupplierModels.ProductImage.objects.filter(
                                product=product
                            ).first(),
                        }
                        for product in subcategory.product_set.all()[:4]
                    ],
                }
                for subcategory in self.model.objects.filter(
                    Q(category=self.subcategory.category), ~Q(id=self.subcategory.id)
                )
                if subcategory.product_set.count() > 0
            ],
        }

        context_data["stores"] = {
            "context_name": "stores",
            "results": [
                {
                    "store": store,
                    "products": [
                        {
                            "product": product,
                            "main_image": SupplierModels.ProductImage.objects.filter(
                                product=product
                            ).first(),
                        }
                        for product in SupplierModels.Product.objects.all()
                        if store in product.store.all()
                    ][:3],
                }
                for store in SupplierModels.Store.objects.all()[:4]
                if store.store_product.count() > 0
            ],
        }

        context_data["suppliers"] = {
            "context_name": "suppliers",
            "results": AuthModels.Supplier.supplier.all(),
        }

        context_data["price_limits"] = {
            "context_name": "price-limits",
            "results": {
                "min_price": self.request.GET.get("min-price", 0),
                "max_price": self.request.GET.get("max-price", None),
            },
        }

        return context_data


class StoreDetailView(DetailView):
    model = SupplierModels.Store

    def get_products_paginator(self):

        PER_PAGE_COUNT = 20

        self.store_products = self.get_object().store_product.all()

        paginator = Paginator(self.store_products.order_by("-id"), PER_PAGE_COUNT)

        page_num = self.request.GET.get("page", 1)
        return paginator.page(page_num)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        store = self.get_object()

        products_paginator = self.get_products_paginator()

        context["page_obj"] = products_paginator
        context["current_page_number"] = self.request.GET.get("page", 1)

        context["view_name"] = store.name
        context["showrooms"] = {
            "context_name": "showrooms",
            "results": ManagerModels.Showroom.objects.filter(store=store),
        }
        context["products"] = {
            "context-name": "products",
            "results": [
                {
                    "product": product,
                    "supplier": product.store.all().first().supplier,
                    "images": product.productimage_set.all().first(),
                }
                for product in products_paginator.object_list
            ],
        }
        context["product_count"] = {
            "context_name": "product-count",
            "results": store.store_product.count(),
        }
        context["related_stores"] = {
            "context_name": "related-stores",
            "results": SupplierModels.Store.objects.filter(
                Q(supplier=store.supplier), ~Q(id=store.id)
            ).order_by("-id")[:5],
        }
        return context


class StoreListView(ListView):
    model = SupplierModels.Store
    paginate_by = 20

    def get_queryset(self):
        supplier_filter_param = self.request.GET.get("supplier", None)
        if supplier_filter_param:
            supplier = (
                AuthModels.ClientProfile.objects.filter(
                    business_name=supplier_filter_param
                )
                .first()
                .user
            )
            return self.model.objects.filter(supplier=supplier).order_by("-id")

        return super().get_queryset().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["view_name"] = _("Stores")

        context["suppliers"] = {
            "context_name": "suppliers",
            "results": AuthModels.Supplier.supplier.all(),
        }

        return context


class SearchView(View):
    model = SupplierModels.Product
    template_name = "supplier/product_list.html"
    PER_PAGE_COUNT = 20

    def get(self, request):

        return render(
            request, template_name=self.template_name, context=self.get_context_data()
        )

    def get_queryset(self):
        # context['str']
        pass


# dashboard
class DashboardView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/dashboard.html"

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context_data = dict()

        context_data["view_name"] = _("Supplier Dashboard")
        context_data["active_tab"] = "Dashboard"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Stores"),
                    "count": SupplierModels.Store.objects.filter(
                        supplier=self.request.user
                    ).count(),
                },
                {
                    "name": _("Products"),
                    "count": SupplierModels.Product.objects.filter(
                        store__in=SupplierModels.Store.objects.filter(
                            supplier=self.request.user
                        )
                    ).count(),
                },
                {
                    "name": _("Services"),
                    "count": SupplierModels.Service.objects.filter(
                        supplier=self.request.user
                    ).count(),
                },
                {
                    "name": _("Contracts"),
                    "count": PaymentModels.Contract.objects.filter(
                        supplier=self.request.user
                    ).count(),
                },
            ],
        }

        context_data["top_products"] = {
            "context_name": "top-products",
            "results": SupplierModels.Product.objects.all()[
                :4
            ],  # should base on products request table
        }
        return context_data


class ProfileView(View):
    template_name = "supplier/dashboard/profile.html"

    def get(self, request):
        context_data = {
            "profile": AuthModels.ClientProfile.objects.filter(
                user=request.user
            ).first()
        }
        return render(request, self.template_name, context=context_data)


class DashboardProductsView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/manage-product.html"

    def get(self, request):
        return render(request, self.template_name)


class DashboardProductsCreateView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/create-product.html"

    def get(self, request):
        context_data = {
            "stores": SupplierModels.Store.objects.filter(supplier=request.user),
            "subcategories": SupplierModels.ProductSubCategory.objects.all(),
        }
        return render(request, self.template_name, context=context_data)

    def post(self, request, *args, **kwargs):
        if not (
            request.POST.get("name")
            and request.POST.get("store")
            and request.POST.get("sub_category")
            and request.POST.get("description")
            and request.POST.get("currency")
            and request.POST.get("price")
            and request.FILES.get("images")
        ):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("supplier:dashboard-productscreate"))
        # try:
        product = SupplierModels.Product.objects.create(
            name=request.POST.get("name"),
            sub_category=SupplierModels.ProductSubCategory.objects.filter(
                name=request.POST.get("sub_category")
            ).first(),
            description=request.POST.get("description"),
            currency=request.POST.get("currency"),
            price=request.POST.get("price"),
        )
        store = SupplierModels.Store.objects.filter(
            name=request.POST.get("store")
        ).first()
        product.store.add(store)
        if product:
            for file in request.FILES.getlist("images"):
                SupplierModels.ProductImage.objects.create(
                    product=product, image=file
                )

            fields = ("name", "description", "price", "currency")
            instance = product
            modal = SupplierModels.Product
            for field in fields:
                for language in settings.LANGUAGES:
                    try:
                        if language[0] == get_language():
                            # already set
                            continue
                        result = translator.translate(
                            getattr(instance, field), dest=language[0]
                        )
                        for model_field in modal._meta.get_fields():
                            if not model_field.name in f"{field}_{language[0]}":
                                continue

                            if model_field.name == f"{field}_{language[0]}":
                                setattr(instance, model_field.name, result.text)
                                instance.save()
                    except:
                        setattr(
                            instance,
                            f"{field}_{language[0]}",
                            getattr(instance, field),
                        )
                        instance.save()

            # add tags
            for i in range(1, 6):
                tag = request.POST.get(f"tag_{i}", None)
                if not tag:
                    continue

                tag = SupplierModels.ProductTag.objects.create(
                    name=tag, product=product
                )
                fields = ("name",)
                instance = tag
                modal = SupplierModels.ProductTag
                for field in fields:
                    for language in settings.LANGUAGES:
                        try:
                            if language[0] == get_language():
                                # already set
                                continue
                            result = translator.translate(
                                getattr(instance, field), dest=language[0]
                            )
                            for model_field in modal._meta.get_fields():
                                if not model_field.name in f"{field}_{language[0]}":
                                    continue

                                if model_field.name == f"{field}_{language[0]}":
                                    setattr(instance, model_field.name, result.text)
                                    instance.save()
                        except:
                            setattr(
                                instance,
                                f"{field}_{language[0]}",
                                getattr(instance, field),
                            )
                            instance.save()

        messages.add_message(
            request, messages.SUCCESS, _("Product created successfully.")
        )
        return redirect(reverse("supplier:dashboard-productscreate"))
        # except Exception as e:
        #     print(e)
        #     messages.add_message(
        #         request, messages.ERROR, _("An Error occurred. Try Again")
        #     )
        #     return redirect(reverse("supplier:dashboard-productscreate"))


class DashboardStoresView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/manage-store.html"

    def get(self, request):
        return render(request, self.template_name)


class DashboardStoresCreateView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/create-store.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if not (request.POST.get("name") and request.FILES.get("image")):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("supplier:dashboard-storescreate"))

        name = request.POST.get("name")
        image = request.FILES.get("image")

        if SupplierModels.Store.objects.filter(name=name):
            messages.add_message(
                request, messages.ERROR, _("Please use a different store name.")
            )
            return redirect(reverse("supplier:dashboard-storescreate"))

        try:
            store = SupplierModels.Store.objects.create(
                name=name, image=image, supplier=request.user
            )
            messages.add_message(
                request, messages.SUCCESS, _("Store created successfully.")
            )

            fields = ("name",)
            instance = store
            modal = SupplierModels.Store
            for field in fields:
                for language in settings.LANGUAGES:
                    try:
                        if language[0] == get_language():
                            # already set
                            continue
                        result = translator.translate(
                            getattr(instance, field), dest=language[0]
                        )
                        for model_field in modal._meta.get_fields():
                            if not model_field.name in f"{field}_{language[0]}":
                                continue

                            if model_field.name == f"{field}_{language[0]}":
                                setattr(instance, model_field.name, result.text)
                                instance.save()
                    except:
                        setattr(
                            instance, f"{field}_{language[0]}", getattr(instance, field)
                        )
                        instance.save()

            return redirect(reverse("supplier:dashboard-storescreate"))
        except:
            messages.add_message(
                request, messages.ERROR, _("Sorry, an error occurred. Please Try Again")
            )
            return redirect(reverse("supplier:dashboard-storescreate"))


class DashboardContractsView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/contracts.html"

    def get(self, request):
        return render(request, self.template_name)


class DashboardContractsDetailsView(SupplierOnlyAccessMixin, DetailView):
    template_name = "supplier/dashboard/contract-detail.html"
    model = PaymentModels.Contract

    def get(self, request, pk):
        contract = PaymentModels.Contract.objects.filter(pk=pk).first()
        context_data = {
            "contract": contract,
            "receipt": PaymentModels.ContractReceipt.objects.filter(
                contract=contract
            ).first(),
        }
        return render(request, self.template_name, context=context_data)

    def get_queryset(self):
        return self.model.objects.all()


class DashboardServicesView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/services.html"

    def get(self, request):
        return render(request, self.template_name)


class DashboardServicesCreateView(SupplierOnlyAccessMixin, View):
    template_name = "supplier/dashboard/create-service.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if not (
            request.POST.get("name")
            and request.POST.get("description")
            and request.POST.get("currency")
            and request.POST.get("price")
        ):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("supplier:dashboard-servicescreate"))

        name = request.POST.get("name")
        description = request.POST.get("description")
        currency = request.POST.get("currency")
        price = request.POST.get("price")

        if SupplierModels.Service.objects.filter(name=name):
            messages.add_message(
                request, messages.ERROR, _("Please use a different service name.")
            )
            return redirect(reverse("supplier:dashboard-servicescreate"))

        try:
            service = SupplierModels.Service.objects.create(
                name=name,
                description=description,
                currency=currency,
                price=price,
                supplier=request.user,
            )
            messages.add_message(
                request, messages.SUCCESS, _("Service created successfully.")
            )

            fields = ("name", "description", "price", "currency")
            instance = service
            modal = SupplierModels.Service
            for field in fields:
                for language in settings.LANGUAGES:
                    try:
                        if language[0] == get_language():
                            # already set
                            continue
                        result = translator.translate(
                            getattr(instance, field), dest=language[0]
                        )
                        for model_field in modal._meta.get_fields():
                            if not model_field.name in f"{field}_{language[0]}":
                                continue

                            if model_field.name == f"{field}_{language[0]}":
                                setattr(instance, model_field.name, result.text)
                                instance.save()
                    except:
                        setattr(
                            instance, f"{field}_{language[0]}", getattr(instance, field)
                        )
                        instance.save()

            return redirect(reverse("supplier:dashboard-servicescreate"))
        except:
            messages.add_message(
                request, messages.ERROR, _("Sorry, an error occurred. Please Try Again")
            )
            return redirect(reverse("supplier:dashboard-servicescreate"))
