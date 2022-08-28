# django
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# python
import os
import uuid
import string

# utility functions
def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s-%s.%s" % (instance.get_username(), uuid.uuid4(), ext)
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SUPPORT = "SUPPORT", "Support"
        SUPPLIER = "SUPPLIER", "Supplier"
        BUYER = "BUYER", "Buyer"

    base_type = Role.SUPPLIER

    account_type = models.CharField(
        _("Account Type"), max_length=50, choices=Role.choices
    )

    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
        blank=True,
        null=True,
        default="test/profiledefault.png",
    )
    is_email_activated = models.BooleanField(_("Email Activated"), default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_email_activated = True

        if self.is_email_activated:
            self.is_active = True
        else:
            self.is_active = False

        if not self.pk:
            self.account_type = self.base_type
        super().save(*args, **kwargs)

    def __str__(self):
        if self.get_username:
            return f"{self.get_username()}"
        return f"{self.first_name} {self.last_name}"


class ClientProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    business_name = models.CharField(_("Business Name"), max_length=256)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    business_description = models.TextField(_("Business Description"))
    country = models.CharField(_("Country"), max_length=256)
    country_code = models.CharField(_("Country Code"), max_length=20)
    city = models.CharField(_("City"), max_length=256)
    mobile_user = models.CharField(_("Number"), max_length=20)
    vat_number = models.CharField(_("VAT Number"), blank=True, null=True, max_length=20)
    legal_etity_identifier = models.CharField(
        _("Legal Entity Identifier"), max_length=256, blank=True, null=True
    )
    website = models.URLField(_("Website"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.business_name:
            self.business_name = self.user.username

        self.slug = slugify(self.business_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_username()}"


class SupplierManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(account_type=User.Role.SUPPLIER)


class Supplier(User):

    base_type = User.Role.SUPPLIER
    supplier = SupplierManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        # since we have a onetoonerel between ClientProfile and User(Supplier)
        # we can access clientprofile
        return self.clientprofile

    def save(self, *args, **kwargs):
        # check if instance is already existing
        if not self.pk:
            self.account_type = self.base_type
            super().save(*args, **kwargs)


class BuyerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(account_type=User.Role.BUYER)


class Buyer(User):

    base_type = User.Role.BUYER
    buyer = BuyerManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.clientprofile

    def save(self, *args, **kwargs):
        # check if instance is already existing
        if not self.pk:
            self.account_type = self.base_type
            super().save(*args, **kwargs)


class SupportProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    responses = models.IntegerField(_("Responses to clients"))


class SupportManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(account_type=User.Role.SUPPORT)


class Support(User):

    base_type = User.Role.SUPPORT
    support = SupportManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.supportprofile

    def save(self, *args, **kwargs):
        # check if instance is already existing
        if not self.pk:
            self.account_type = self.base_type
            super().save(*args, **kwargs)
