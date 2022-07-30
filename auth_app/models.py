# django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


# python
import os
import uuid


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

    base_type = Role.ADMIN

    account_type = models.CharField(
        _("Account Type"), max_length=50, choices=Role.choices
    )

    image = models.ImageField(
        verbose_name=_("Image"), upload_to=get_file_path, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        # check if instance is already existing
        if not self.pk:
            # by default is admin
            if self.base_type == self.Role.ADMIN:
                self.is_superuser = True
            else:
                self.is_active = False
            self.account_type = self.base_type
            super().save(*args, **kwargs)

    def __str__(self):
        if self.get_username:
            return f"{self.get_username()}"
        return f"{self.first_name} {self.last_name}"


class ClientProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    country = models.CharField(_("Country"), max_length=256)
    country_code = models.IntegerField(_("Country Code"))
    city = models.CharField(_("City"), max_length=256)
    mobile_user = models.CharField(_("Number"), max_length=12)
    vat_number = models.IntegerField(_("VAT Number"), blank=True, null=True)
    legal_etity_identifier = models.CharField(
        _("Legal Entity Identifier"), max_length=256, blank=True, null=True
    )
    website = models.URLField(_("Website"), blank=True, null=True)


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
