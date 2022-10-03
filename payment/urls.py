from django.urls import path

app_name = "payment"

from payment import views

urlpatterns = [
    path("memberships/", 
        views.InitSubscriptionView.as_view(), name="memberships"),
    path(
        "memberships/<str:slug>",
        views.MembershipsDetailsView.as_view(),
        name="memberships-details",
    ),
    path(
        "completePaypalPayment/",
        views.CompletePaypalPaymentView.as_view(),
        name="completePaypalPayment",
    ),
    path(
        "stripeCreateCheckoutSession/<int:pk>",
        views.StripeCreateCheckoutSessionView.as_view(),
        name="stripeCreateCheckoutSession",
    ),
    # path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    # path("checkout/", views.checkout_page, name='checkout'),
    path("braintree/payments/<int:pk>", views.payment, name="braintree-payment"),
    path("gPayPayment/<int:pk>", views.gPayPayment, name="gPayPayment"),
    path(
        "contracts/payments/<int:pk>",
        views.ContractPaymentView.as_view(),
        name="contract-payment",
    ),
    path("contracts/receipt/<int:pk>", views.contract_receipt, name="contract-receipt"),
    path(
        "initial/subscription/",
        views.InitSubscriptionView.as_view(),
        name="init-subscription",
    ),
]
