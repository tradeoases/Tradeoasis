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
import string

# apps
from auth_app.models import Supplier

# utility functions
def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    # filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    filename = f'{instance.slug}-{uuid.uuid4()}'[:50] + f'.{ext}'
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
        _("Safe Url"), unique=True, blank=True, null=True, max_length=200
    )

    image = models.FileField(
        verbose_name=_("Service Image"),
        upload_to=get_file_path,
        default="test/django.png",
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:200]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class ProductCategory(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    product_count = models.IntegerField(_("Number of products"), default=0)
    image = models.FileField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
        default="test/django.png",
    )
    slug = models.SlugField(
        _("Safe Url"), unique=True, blank=True, null=True, max_length=200
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:200]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class ProductSubCategory(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    image = models.FileField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
        default="test/django.png",
    )
    slug = models.SlugField(
        _("Safe Url"), unique=True, blank=True, null=True, max_length=200
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:200]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    # can be in many stores
    store = models.ManyToManyField(to=Store, related_name="store_product")
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    sub_category = models.ForeignKey(
        to=ProductSubCategory,
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=12)
    currency = models.CharField(_("Currency"), max_length=6)
    slug = models.SlugField(
        _("Safe Url"), unique=True, blank=True, null=True, max_length=200
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:200]

        if not self.pk:
            self.category = self.sub_category.category

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.FileField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
    )
    slug = models.SlugField(
        _("Safe Url"), unique=True, blank=True, null=True, max_length=100
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.product.name}-{uuid.uuid4()}")[:50]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name}"


class ProductTag(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:50]

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name}"


class Service(models.Model):
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=122)
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
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:50]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


# SIGNALS
@receiver(post_save, sender=Product)
def on_product_save(sender, instance, **kwargs):
    product_sub_category = instance.sub_category
    # category product count increases
    product_sub_category.category.product_count += 1
    product_sub_category.category.save()
    product_sub_category.save()


@receiver(post_delete, sender=Product)
def delete_product(sender, instance, *args, **kwargs):
    images = ProductImage.objects.filter(product=instance)
    for image in images:
        image.delete()

    product_sub_category = instance.sub_category
    # category product count decreases
    product_sub_category.category.product_count -= 1
    product_sub_category.category.save()
    product_sub_category.save()


@receiver(post_delete, sender=Store)
def delete_store(sender, instance, *args, **kwargs):
    if instance.image and instance.image != "test/django.png":
        instance.image.delete()
