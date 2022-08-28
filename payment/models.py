from ast import expr
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# python
import datetime
from dateutil.relativedelta import relativedelta
import string
import uuid

# apps
from auth_app.models import Buyer, Supplier
from supplier.models import Service


class MembershipPlan(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=6)
    currency = models.CharField(_("Currency"), max_length=6)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:50]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class Features(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    membership = models.ManyToManyField(to=MembershipPlan, related_name="features")

    def __str__(self) -> str:
        return f"{self.name}"


class Membership(models.Model):

    PLAN_DURATION = (
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Annually", "Annually"),
    )
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    plan = models.ForeignKey(to=MembershipPlan, on_delete=models.CASCADE)
    expiry_date = models.DateField(_("Plan expiry date"), blank=True, null=True)
    duration = models.CharField(_("Duration"), max_length=256, choices=PLAN_DURATION)
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def __str__(self) -> str:
        return f"User: {self.supplier.username}, Plan: {self.plan.name}"


def get_expiry_date(duration):
    if duration == "Monthly":
        return (datetime.date.today() + relativedelta(months=1)).strftime("%Y-%m-%d")
    elif duration == "Quarterly":
        return (datetime.date.today() + relativedelta(months=4)).strftime("%Y-%m-%d")
    elif duration == "Annually":
        return (datetime.date.today() + relativedelta(years=1)).strftime("%Y-%m-%d")
    else:
        pass


# set expiry date
@receiver(post_save, sender=Membership)
def send_membership_expiry(sender, instance, **kwargs):
    if not instance.expiry_date:
        generated_expiry_date = get_expiry_date(instance.duration)
        instance.expiry_date = generated_expiry_date
        instance.save()


class ModeOfPayment(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    transaction_count = models.IntegerField(_("Number of transactions"), default=0)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:50]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class MembershipReceipt(models.Model):
    membership = models.ForeignKey(to=Membership, on_delete=models.CASCADE)
    model_of_payment = models.ForeignKey(to=ModeOfPayment, on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=256)
    payment_id = models.CharField(_("Payment Id"), max_length=256)
    amount_paid = models.DecimalField(
        _("Total Amount Paid"), decimal_places=2, max_digits=12
    )
    currency = models.CharField(_("Currency"), max_length=6)
    reference_id = models.CharField(
        _("reference_id"), max_length=20, blank=True, null=True
    )
    # authorizations_id = models.CharField(_("authorizations_id"), max_length=20)
    status = models.CharField(_("status"), max_length=20, default="NOT APPROVED")

    def __str__(self) -> str:
        return f"User: {self.payment_id}"


# set expiry date
@receiver(post_save, sender=MembershipReceipt)
def record_transaction_count(sender, instance, **kwargs):
    mode_of_payment = instance.model_of_payment
    # category product count increases
    mode_of_payment.transaction_count = int(mode_of_payment.transaction_count) + 1
    mode_of_payment.save()


class Contract(models.Model):
    supplier = models.ForeignKey(
        to=Supplier, on_delete=models.CASCADE, related_name="supplier"
    )
    buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE, related_name="buyer")

    service = models.ForeignKey(
        to=Service, on_delete=models.CASCADE, related_name="supplier_service"
    )

    is_complete = models.BooleanField(_("Contract completed"), default=False)

    is_accepted = models.BooleanField(_("Contract accepted"), default=False)

    created_on = models.DateField(_("Created on"), default=timezone.now)

    def __str__(self) -> str:
        return f"Supplier: {self.supplier.username}, Buyer: {self.buyer.username}"


class ContractReceipt(models.Model):
    contract = models.ForeignKey(
        to=Contract,
        on_delete=models.CASCADE,
    )
    model_of_payment = models.ForeignKey(to=ModeOfPayment, on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=256)
    payment_id = models.CharField(_("Payment Id"), max_length=256)
    amount_paid = models.DecimalField(
        _("Total Amount Paid"), decimal_places=2, max_digits=12
    )
    currency = models.CharField(_("Currency"), max_length=6)

    def __str__(self) -> str:
        return f"User: {self.payment_id}"
