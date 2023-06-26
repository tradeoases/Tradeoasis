from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib import messages

from auth_app import models as AuthModels
from payment import models as PaymentModels
from supplier import models as SupplierModels
from buyer import models as BuyerModels

from buyer.mixins import BuyerOnlyAccessMixin

from django.utils.translation import get_language
from googletrans import Translator
from django.conf import settings

translator = Translator()

from auth_app import forms as AuthForms


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


class EditAccountsProfileView(BuyerOnlyAccessMixin, View):
    template_name = "buyer/dashboard/account_edit.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if not (
            request.POST.get("first_name")
            and request.POST.get("last_name")
            and request.POST.get("username")
            and request.POST.get("email")
        ):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("buyer:dashboard-editaccountsprofile"))

        if (
            request.POST.get("first_name") == request.user.first_name
            and request.POST.get("last_name") == request.user.last_name
            and request.POST.get("username") == request.user.username
            and request.POST.get("email") == request.user.email
        ):
            messages.add_message(
                request, messages.ERROR, _("No modification was made.")
            )
            return redirect(reverse("buyer:dashboard-editaccountsprofile"))

        if (
            AuthModels.User.objects.filter(username=request.POST.get("username"))
            and request.POST.get("username") != request.user.username
        ):
            messages.add_message(request, messages.ERROR, _("Username not available."))
            return redirect(reverse("buyer:dashboard-editaccountsprofile"))

        if (
            AuthModels.User.objects.filter(email=request.POST.get("email"))
            and request.POST.get("email") != request.user.email
        ):
            messages.add_message(request, messages.ERROR, _("Email not available."))
            return redirect(reverse("buyer:dashboard-editaccountsprofile"))

        form = AuthForms.UserUpdateFormManager(data=request.POST, instance=request.user)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, _("Invalid data. Try again."))
            return redirect(reverse("buyer:dashboard-editaccountsprofile"))
        form.save()

        fields = ("first_name", "last_name")
        instance = request.user
        modal = AuthModels.User
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
        messages.add_message(
            request, messages.SUCCESS, _("Account Details Editted Successfully")
        )
        return redirect(reverse("buyer:profile"))


def password_reset(request):
    if request.method == "GET":
        return render(request, "buyer/dashboard/password_reset.html")

    if request.method == "POST":
        if request.POST.get("new_password") != request.POST.get("confirm_new_password"):
            messages.add_message(request, messages.ERROR, _("Password mismatch."))
            return redirect(reverse("buyer:password-reset"))

        # confirm current password
        user = authenticate(
            username=request.user.username,
            password=request.POST.get("current_password"),
        )
        if not user:
            messages.add_message(
                request, messages.ERROR, _("Wrong current password entered.")
            )
            return redirect(reverse("buyer:password-reset"))

        if authenticate(
            username=request.user.username, password=request.POST.get("new_password")
        ):
            messages.add_message(request, messages.ERROR, _("No modification made."))
            return redirect(reverse("buyer:password-reset"))

        # make password
        generated_password = make_password(request.POST.get("new_password"))
        user = AuthModels.User.objects.filter(pk=request.user.pk).first()
        user.password = generated_password
        user.save()
        messages.add_message(
            request, messages.SUCCESS, _("Account password reset successfully")
        )
        return redirect(reverse("buyer:profile"))


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


class EditBusinessProfileView(BuyerOnlyAccessMixin, View):
    template_name = "buyer/dashboard/business_edit.html"

    def get(self, request, slug):
        context_data = {
            "profile": AuthModels.ClientProfile.objects.filter(slug=slug).first()
        }
        return render(request, self.template_name, context=context_data)

    def post(self, request, slug):
        profile = AuthModels.ClientProfile.objects.filter(slug=slug).first()
        required_fields = [
            request.POST.get("business_name", None),
            request.POST.get("business_description", None),
            request.POST.get("country", None),
            request.POST.get("city", None),
        ]

        if None in required_fields:
            messages.add_message(
                request,
                messages.ERROR,
                "{}".format(_("Please Fill all reqiured fields.")),
            )
            return redirect(reverse("buyer:dashboard-editbusinessprofile", args=[slug]))

        try:
            form = AuthForms.UserProfileUpdateFormManager(
                data=request.POST, instance=profile
            )
            if not form.is_valid():
                messages.add_message(
                    request, messages.ERROR, _("Invalid data. Try again.")
                )
                return redirect(reverse("buyer:dashboard-editaccountsprofile"))
            form.save()

            fields = (
                "business_name",
                "business_description",
                "country",
                "country_code",
                "city",
                "mobile_user",
            )
            instance = profile
            modal = AuthModels.ClientProfile
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

            messages.add_message(
                request, messages.SUCCESS, _("Business Details Editted Successfully.")
            )
            return redirect(reverse("buyer:business"))
        except Exception as e:
            print(e)
            messages.add_message(
                request, messages.ERROR, _("An Error Occurred. Try Again.")
            )
            return redirect(reverse("buyer:dashboard-editbusinessprofile", args=[slug]))


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

class OrdersView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/orders.html"

    def get(self, request):
        return render(request, self.template_name)


class OrderDetailsView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/order-details.html"

    def get(self, request):
        return render(request, self.template_name)


class RequestForQuoteView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/request-for-quote.html"

    def get(self, request):
        return render(request, self.template_name)


class OrderHistoryView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/order-history.html"

    def get(self, request):
        return render(request, self.template_name)


class OrderTrackingView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/order-tracking.html"

    def get(self, request):
        return render(request, self.template_name)



class MessengerView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/messenger.html"

    def get(self, request):
        return render(request, self.template_name)



class DashboardView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/dashboard.html"

    def get(self, request):
        return render(request, self.template_name)


class CalendarView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/calendar.html"

    def get(self, request):
        return render(request, self.template_name)


class NotificationsView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/notifications.html"

    def get(self, request):
        return render(request, self.template_name)

class BidsView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/bids.html"

    def get(self, request):
        return render(request, self.template_name)


class BidsCompareView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/bids-compare.html"

    def get(self, request):
        return render(request, self.template_name)

class BidsView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/bids.html"

    def get(self, request):
        return render(request, self.template_name)

class ReportingAnalyticsView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/reporting-analytics.html"

    def get(self, request):
        return render(request, self.template_name)

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





#---------------------------------------- WishList ----------------------------------------
class WishListListView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/wishlist.html"
    model = SupplierModels.WishListProduct

    def get_queryset(self):
        business = AuthModels.ClientProfile.objects.filter(user = self.request.user)
        return self.model.objects.filter(buyer=business.first())

@method_decorator(csrf_exempt, name='dispatch')
class WishListAppeendAppendView(BuyerOnlyAccessMixin, View):
    model = SupplierModels.WishListProduct

    def post(self, request, product_slug):
        product = get_object_or_404(SupplierModels.Product, slug=product_slug)
        business = AuthModels.ClientProfile.objects.filter(user = self.request.user)
        
        self.model.objects.create(
            buyer = business.first(),
            product = product
        )
        return redirect(reverse("buyer:wishlist"))

@method_decorator(csrf_exempt, name='dispatch')
class WishListDeleteProductView(BuyerOnlyAccessMixin, View):
    model = SupplierModels.WishListProduct

    def post(self, request, product_slug):
        product = get_object_or_404(SupplierModels.Product, slug=product_slug)
        business = AuthModels.ClientProfile.objects.filter(user = self.request.user)
        
        wishlist_product = self.model.objects.filter(product = product, buyer=business.first())
        if wishlist_product:
            wishlist_product.first().delete()
        return redirect(reverse("buyer:wishlist"))

# cart
class CartListView(BuyerOnlyAccessMixin, ListView):
    template_name = "buyer/dashboard/cartlist.html"
    model = BuyerModels.Cart

    def get_queryset(self):
        business = AuthModels.ClientProfile.objects.filter(user=self.request.user).first()
        cart = self.model.objects.filter(buyer=business)
        if not cart:
            cart = BuyerModels.Cart.objects.create(buyer=business)
        else:
            cart = cart.first()

        return SupplierModels.OrderProductVariation.objects.filter(cart=cart)