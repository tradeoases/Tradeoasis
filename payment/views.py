from crypt import methods
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import json, os

from supplier import models as SupplierModels
from auth_app import models as AuthModels
from manager import models as ManagerModels
from payment import models as PaymentModels
from payment.mixins import AuthedOnlyAccessMixin

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

# payments
import braintree
from django.conf import settings

# from . import forms

from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient
import stripe

from django.utils.translation import get_language
from googletrans import Translator
from django.conf import settings

translator = Translator()


class MembershipsView(View):
    model = PaymentModels.MembershipPlan
    template_name = "payments/memberships.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = dict()

        context["view_name"] = _("Memberships")

        context["memberships"] = {
            "context_name": "memberships",
            "results": [
                {"plan": plan, "features": plan.features.all()}
                for plan in PaymentModels.MembershipPlan.objects.all()
            ],
        }
        return context


class MembershipsDetailsView(AuthedOnlyAccessMixin, DetailView):
    model = PaymentModels.MembershipPlan
    template_name = "payments/membership_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        plan = self.get_object()

        context["view_name"] = _("Memberships")

        context["features"] = {
            "context_name": "features",
            "results": plan.features.all(),
        }
        context["STRIPE_PUBLIC_KEY"] = os.environ.get("STRIPE_PUBLIC_KEY")

        # braintree

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        # Configure Braintree
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )

        try:
            braintree_client_token = braintree.ClientToken.generate(
                {"customer_id": self.request.user.id}
            )
        except:
            braintree_client_token = braintree.ClientToken.generate({})

        context["braintree_client_token"] = braintree_client_token

        return context


class CompletePaypalPaymentView(AuthedOnlyAccessMixin, View):
    def post(self, request):
        PPClient = PayPalClient()

        body = json.loads(request.body)

        orderID = body["orderID"]
        payerID = body["payerID"]
        paymentID = body["paymentID"]
        paymentSource = body["paymentSource"]
        plan_id = body["plan"]

        # get payment for paypal that matched the orderID
        requestorder = OrdersGetRequest(orderID)
        response = PPClient.client.execute(requestorder)

        # CREATED, SAVED, APPROVED, VOIDED, COMPLETED, PAYER_ACTION_REQUIRED
        if response.result.status in ("APPROVED", "CREATED"):
            if request.user.account_type == "SUPPLIER":
                membership = PaymentModels.Membership(
                    supplier=request.user,
                    plan=PaymentModels.MembershipPlan.objects.filter(
                        id=plan_id
                    ).first(),
                    duration="Monthly",
                )
                membership.save()

                # 'amount', 'dict', 'payee', 'reference_id', 'shipping'

                if membership:
                    receipt = PaymentModels.MembershipReceipt(
                        membership=membership,
                        model_of_payment=PaymentModels.ModeOfPayment.objects.filter(
                            name="Paypal"
                        ).first(),
                        address=response.result.purchase_units[
                            0
                        ].shipping.address.address_line_1,
                        payment_id=orderID,
                        amount_paid=float(
                            response.result.purchase_units[0].amount.value
                        ),
                        currency=response.result.purchase_units[0].amount.currency_code,
                        reference_id=response.result.purchase_units[0].reference_id,
                        status=response.result.status,
                    )
                    receipt.save()
            if membership and receipt:

                # send email

                return HttpResponse(status=204)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()


class StripeCreateCheckoutSessionView(View):
    def post(self, request, pk):

        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        plan = PaymentModels.MembershipPlan.objects.filter(id=pk).first()

        if plan.name == "Gold":
            price_id = "price_1LZejtF6gkT4kB8Uf2hdHR8b"
        if plan.name == "Silver":
            price_id = "price_1LZejjF6gkT4kB8UtRdTnERG"
        if plan.name == "Bronze":
            price_id = "price_1LZejVF6gkT4kB8UhPcFJ1MI"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("manager:home")),
            cancel_url=request.build_absolute_uri(reverse("payments:memberships")),
        )
        return JsonResponse({"id": checkout_session.id})


@login_required
def payment(request, pk):
    plan = PaymentModels.MembershipPlan.objects.filter(id=pk).first()
    if plan:
        nonce_from_the_client = request.POST["paymentMethodNonce"]
        customer_kwargs = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }
        customer_create = braintree.Customer.create(customer_kwargs)
        customer_id = customer_create.customer.id
        result = braintree.Transaction.sale(
            {
                "amount": plan.price,
                "payment_method_nonce": nonce_from_the_client,
                "options": {"submit_for_settlement": True},
            }
        )

        # timestamp, status, amount, user
        if result.status in ("submitted_for_settlement"):
            if request.user.account_type == "SUPPLIER":

                plan = PaymentModels.Membership.objects.filter(
                    supplier=request.user,
                    plan=PaymentModels.MembershipPlan.objects.filter(id=pk).first(),
                )
                if plan:
                    messages.add_message(
                        request, messages.ERROR, _("Membership already exists.")
                    )
                    return redirect(
                        reverse(
                            "payments:memberships-details", kwargs={"slug": plan.slug}
                        )
                    )

                membership = PaymentModels.Membership(
                    supplier=request.user,
                    plan=PaymentModels.MembershipPlan.objects.filter(id=pk).first(),
                    duration="Monthly",
                )
                membership.save()

                if membership:
                    receipt = PaymentModels.MembershipReceipt(
                        membership=membership,
                        model_of_payment=PaymentModels.ModeOfPayment.objects.filter(
                            name="Braintree"
                        ).first(),
                        address=result.transaction.id,
                        payment_id=result.transaction.id,
                        amount_paid=float(result.transaction.amount),
                        currency=result.transation.currency_iso_code,
                        reference_id=result.transation.retrieval_reference_number,
                        status=result.transation.status,
                    )
                    receipt.save()

                if membership and receipt:
                    # send email

                    return HttpResponse(status=204)
                else:
                    return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()


def gPayPayment(request):
    plan = PaymentModels.MembershipPlan.objects.filter(id=pk).first()
    if plan:
        nonce_from_the_client = request.POST["paymentMethodNonce"]
        type = request.POST["type"]
        paymentData = request.POST["paymentData"]

        customer_kwargs = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }

        customer_create = braintree.Customer.create(customer_kwargs)
        customer_id = customer_create.customer.id

        if type == "AndroidPayCard":
            result = braintree.transaction.sale(
                {
                    "amount": "{}".format(plan.amount),
                    "payment_method_nonce": nonce_from_the_client,
                    "device_data": paymentData.get("deviceData"),
                    "options": {"submit_for_settlement": True},
                    "billing": {
                        "postal_code": paymentData.get("postalCode"),
                    },
                }
            )

        if type == "PayPalAccount":
            result = braintree.transaction.sale(
                {
                    "amount": "{}".format(plan.amount),
                    "payment_method_nonce": paymentData.get("payment_method_nonce"),
                    "device_data": paymentData.get("device_data"),
                    "order_id": "Mapped to PayPal Invoice Number",
                    "options": {
                        "submit_for_settlement": True,
                        "paypal": {
                            "custom_field": "PayPal custom field",
                            "description": "Description for PayPal email receipt",
                        },
                    },
                }
            )
            if result.is_success:
                "Success ID: ".format(result.transaction.id)
            else:
                format(result.message)

    else:
        return HttpResponseNotFound()


class InitSubscriptionView(View):
    template_name = 'payments/initsubscription.html'


    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("auth_app:login"))

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        # Configure Braintree
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )

        try:
            braintree_client_token = braintree.ClientToken.generate(
                {"customer_id": self.request.user.id}
            )
        except:
            braintree_client_token = braintree.ClientToken.generate({})


        context_data = {
            "view_name": _("Business Profile"),
            "braintree_client_token" : braintree_client_token
        }

        return render(request, self.template_name, context=context_data)


class ContractPaymentView(View):
    template_name = "payments/contract_payment.html"

    def get(self, request, pk):
        contract = PaymentModels.Contract.objects.filter(pk=pk).first()

        context_data = dict()
        context_data['view_name'] = "Contract Payment"
        context_data['contract'] = contract

        return render(request, self.template_name, context=context_data)

def contract_receipt(request, pk):
    if request.method == "GET":

        contract = PaymentModels.Contract.objects.filter(pk=pk).first()
        context_data = dict()
        context_data['view_name'] = "Contract Payment"
        context_data['contract'] = contract

        return render(request, "payments/contract_ receipt.html", context=context_data)
        # pdf = render_to_pdf('payments/contract_ receipt.html', context_data)
        # return HttpResponse(pdf, content_type='application/pdf')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None