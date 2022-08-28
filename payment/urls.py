from django.urls import path

app_name = "payment"

from payment import views

urlpatterns = [
    path("memberships/", views.MembershipsView.as_view(), name="memberships"),
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
]
