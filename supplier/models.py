# django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# python
import os
import uuid

# apps
from auth_app.models import Supplier

# utility functions
def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)


class Store(models.Model):
    name = models.CharField(_("Store Name"), max_length=256)
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
    )
    # location = models.ManyToManyField(
    #     to=Location,
    #     related_name='store_locations',
    #     default=None
    # )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    
    image = models.ImageField(
        verbose_name=_("Service Image"),
        upload_to=get_file_path,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return f"{self.name}"


class ProductCategory(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    product_count = models.IntegerField(_("Number of products"), default=0)
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    # can be in many stores
    store = models.ManyToManyField(to=Store, related_name="store_product")
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(_("Price"), decimal_places=3, max_digits=6)
    currency = models.CharField(_("Currency"), max_length=6)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.product.name}-image")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name}"


# SIGNALS
@receiver(post_save, sender=Product)
def on_product_save(sender, instance, **kwargs):
    product_category = instance.category
    # category product count increases
    product_category.product_count = int(product_category.product_count) + 1
    product_category.save()


class Service(models.Model):
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    price = models.DecimalField(_("Price"), decimal_places=3, max_digits=12)
    currency = models.CharField(_("Currency"), max_length=6)
    contract_count = models.IntegerField(_("Number of contracts"), default=0)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


@receiver(post_delete, sender=Store)
def delete_store_image(sender, instance, *args, **kwargs):
    instance.photo.delete(save=True)


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, *args, **kwargs):
    images = ProductImage.objects.filter(product=instance)
    for image in images:
        image.delete()
