from audioop import reverse
from unicodedata import category
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.utils.translation import gettext as _
from django.contrib import messages

from auth_app import models as AuthModels
from supplier import models as SupplierModels
from buyer import models as BuyerModels
from manager import models as ManagerModels
from payment import models as PaymentModels

from manager import forms as ManagerForms


class AdminDashboardView(View):
    template_name = "app_admin/index.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard")
        context_data["active_tab"] = "Home"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Total Suppliers"),
                    "description": _("Total Supplier Count"),
                    "count": AuthModels.Supplier.supplier.all().count(),
                },
                {
                    "name": _("Total Buyers"),
                    "description": _("Total Buyer Count"),
                    "count": AuthModels.Buyer.buyer.all().count(),
                },
                {
                    "name": _("Total Product"),
                    "description": _("Total Product Count"),
                    "count": SupplierModels.Product.objects.all().count(),
                },
                {
                    "name": _("Total Showrooms"),
                    "description": _("Showroom Count"),
                    "count": ManagerModels.Showroom.objects.all().count(),
                },
                {
                    "name": _("Total Stores"),
                    "description": _("Total Store Count"),
                    "count": ManagerModels.Store.objects.all().count(),
                },
                {
                    "name": _("Total Memberships"),
                    "description": _("Memberships"),
                    "count": PaymentModels.Membership.objects.all().count(),
                },
                {
                    "name": _("Total Contracts"),
                    "description": _("Contract Created"),
                    "count": PaymentModels.Contract.objects.all().count(),
                },
            ],
        }

        context_data["top_suppliers"] = {
            "context_name": "top-suppliers",
            "results": AuthModels.Supplier.supplier.all()[:4],
        }
        context_data["recent_payments"] = {
            "context_name": "recent-payments",
            "results": PaymentModels.Membership.objects.all().order_by("-id")[:4],
        }
        return context_data


class AdminClientsView(View):
    template_name = "app_admin/clients.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard")
        context_data["active_tab"] = "Clients"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Total Suppliers"),
                    "description": _("Total Supplier Count"),
                    "count": AuthModels.Supplier.supplier.all().count(),
                },
                {
                    "name": _("Total Buyers"),
                    "description": _("Total Buyer Count"),
                    "count": AuthModels.Buyer.buyer.all().count(),
                },
                {
                    "name": _("Total Product"),
                    "description": _("Total Product Count"),
                    "count": SupplierModels.Product.objects.all().count(),
                },
                {
                    "name": _("Total Contracts"),
                    "description": _("Contract Created"),
                    "count": PaymentModels.Contract.objects.all().count(),
                },
            ],
        }

        context_data["top_suppliers"] = {
            "context_name": "top-suppliers",
            "results": AuthModels.Supplier.supplier.all()[:6],
        }
        context_data["top_buyers"] = {
            "context_name": "top-buyers",
            "results": AuthModels.Buyer.buyer.all()[:6],
        }
        return context_data


class AdminManagersView(View):
    template_name = "app_admin/manager.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Clients")
        context_data["active_tab"] = "Manager"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Total Showrooms"),
                    "description": _("Showroom Count"),
                    "count": ManagerModels.Showroom.objects.all().count(),
                },
                {
                    "name": _("Total Stores"),
                    "description": _("Total Store Count"),
                    "count": ManagerModels.Store.objects.all().count(),
                },
                {
                    "name": _("Total Memberships"),
                    "description": _("Memberships"),
                    "count": PaymentModels.Membership.objects.all().count(),
                },
                {
                    "name": _("Total Services"),
                    "description": _("Total Services Count"),
                    "count": ManagerModels.Service.objects.all().count(),
                },
            ],
        }
        return context_data


class ServiceCreateView(CreateView):
    template_name = "app_admin/service_create.html"
    model = ManagerModels.Service
    fields = ["name", "description"]

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not (name and description):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("app_admin:service-create"))

        form = ManagerForms.ServiceFormManager(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, _("Invalid Data Entered."))
            return redirect(reverse("app_admin:service-create"))

        form.save()
        messages.add_message(
            request, messages.SUCCESS, _(f"Service ({name}) created successfully.")
        )
        return redirect(reverse("app_admin:service-create"))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["view_name"] = _("Admin Dashboard - Manager")
        context_data["active_tab"] = "Manager"
        return context_data


class ShowroomCreateView(CreateView):
    template_name = "app_admin/showroom_create.html"
    model = ManagerModels.Showroom
    fields = ["name", "location", "image"]

    def post(self, request):
        name = request.POST.get("name")
        image = request.FILES.get("image")

        if not (name and image):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("app_admin:showroom-create"))

        showroom = ManagerModels.Showroom.objects.create(name=name, image=image)

        if not showroom:
            messages.add_message(request, messages.ERROR, _("Error occured. Try Again"))
            return redirect(reverse("app_admin:showroom-create"))

        messages.add_message(
            request, messages.SUCCESS, _(f"Service ({name}) created successfully.")
        )
        return redirect(reverse("app_admin:showroom-create"))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["view_name"] = _("Admin Dashboard - Manager")
        context_data["active_tab"] = "Manager"
        return context_data


class CategoryCreateView(View):
    template_name = "app_admin/productcategorycreate.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Clients")
        context_data["active_tab"] = "Manager"

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        name = request.POST.get("category-name")
        image = request.FILES.get("category-image")

        category = SupplierModels.ProductCategory.objects.filter(name=name.title())
        if category.exists():
            messages.add_message(
                request, messages.ERROR, _(f"Category({name}) already exists.")
            )
            return redirect(reverse("app_admin:category-create"))

        category = SupplierModels.ProductCategory.objects.create(name=name, image=image)

        # create sub categories if any
        sub_category_len = len(request.FILES) - 1
        for i in range(1, sub_category_len + 1):
            sub_cat_name = request.POST.get(f"subcategory-{i}")
            sub_cat_image = request.FILES.get(f"subcategory-{i}")

            if SupplierModels.ProductSubCategory.objects.filter(
                name=sub_cat_name.title()
            ).exists():
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(f"Sub category ({sub_cat_name}) already exists."),
                )
                continue

            SupplierModels.ProductSubCategory.objects.create(
                name=sub_cat_name, image=sub_cat_image, category=category
            )

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Category ({}) created successfully.").format(name),
        )
        return redirect(reverse("app_admin:category-create"))


class AdminDiscussionsView(View):
    template_name = "app_admin/support/index.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())


class AdminChatView(View):
    template_name = "app_admin/support/chat.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())


class AdminCommunityView(View):
    template_name = "app_admin/support/community.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())


class AdminCommunityChatView(View):
    template_name = "app_admin/support/discussion.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())
