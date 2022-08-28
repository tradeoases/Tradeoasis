from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _
from django.views.generic import ListView

from auth_app import models as AuthModels
from payment import models as PaymentModels

from buyer.mixins import BuyerOnlyAccessMixin


class ProfileView(BuyerOnlyAccessMixin, View):
    template_name = "buyer/dashboard/profile.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Profile")
        context_data["buyer"] = AuthModels.Buyer.buyer.filter(
            id=self.request.user.id
        ).first()

        return context_data


class BusinessProfileView(BuyerOnlyAccessMixin, View):
    template_name = "buyer/dashboard/business-profile.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Profile")
        context_data["buyer"] = AuthModels.Buyer.buyer.filter(
            id=self.request.user.id
        ).first()

        return context_data


class ContractListView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/contracts.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Contracts")
        context_data["contracts"] = PaymentModels.ContractReceipt.objects.filter(
            contract__buyer=self.request.user
        )

        return context_data


class VisitedProductsListView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/products.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Contracts")
        context_data["contracts"] = ""

        return context_data


class DashboardContractsDetailsView(View):
    template_name = "buyer/dashboard/contract-detail.html"
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
