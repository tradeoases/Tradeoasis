# django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Q

# python
import os
import uuid
import string

# apps
from auth_app.models import Supplier, Buyer, ClientProfile

# utility functions
def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    # filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    filename = f"{instance.slug}-{uuid.uuid4()}"[:50] + f".{ext}"
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)


# utility functions
def get_video_path(instance, filename):
    ext = filename.split(".")[-1]
    # filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    filename = f"{instance.slug}-{uuid.uuid4()}"[:50] + f".{ext}"
    return os.path.join(f"{instance.__class__.__name__}/video/", filename)

# global model managers

class VerifiedManager(models.Manager):
    def get_queryset(self):
        # Override the default queryset to exclude inactive items
        return super().get_queryset().filter(is_verified=True)


class AdminListManager(models.Manager):
    def get_queryset(self):
        # Override the default queryset to exclude inactive items
        return super().get_queryset().all()

class Store(models.Model):
    objects = VerifiedManager()
    admin_list = AdminListManager()

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
    is_verified = models.BooleanField(_("Verified by Admin"), default=False)
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:200]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


#======================================= Product =======================================
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
    objects = VerifiedManager()
    admin_list = AdminListManager()
    class Meta:
        ordering = ["-id"]

    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    # for easy querying supplier attribute has been added
    business = models.ForeignKey(
        to=ClientProfile,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    # can be in many stores
    store = models.ManyToManyField(to=Store, related_name="store_product", blank=True)
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    sub_category = models.ForeignKey(
        to=ProductSubCategory,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    slug = models.SlugField(
        _("Safe Url"), unique=True, blank=True, null=True, max_length=200
    )
    currency = models.CharField(_("Currency"), max_length=6, blank=True, null=True)
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=12, blank=True, null=True)
    discount = models.DecimalField(_("Discount as a Percentage"), decimal_places=2, max_digits=3, blank=True, null=True)
    stock = models.IntegerField(_("stock"), blank=True, null=True)
    is_verified = models.BooleanField(_("Verified by Admin"), default=False)
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.name) not in self.slug:
            self.slug = slugify(f"{self.name}{uuid.uuid4()}")[:200]
        self.category = self.sub_category.category

        self.name = self.name

        super().save(*args, **kwargs)

    def sell_made(self, items_sold):
        if self.stock > 0:
            self.stock -= items_sold
            self.save()
        else:
            raise ValueError(_('Items sold are more than available stock'))

    @property
    def supplier(self):
        if not self.store.all():
            return self.business
        return self.store.all().first().supplier.profile
        
    @property
    def stores(self):
        if not self.store.all():
            return None
        return self.store.all()

    def __str__(self) -> str:
        return f"{self.name} {self.supplier}"



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
        self.slug = slugify(f"{self.product.name[:10]}-{uuid.uuid4()}")[:50] + "-images"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name}"

class ProductVideo(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    video = models.FileField(
        verbose_name=_("Video"),
        upload_to=get_video_path,
    )
    slug = models.SlugField(
        _("Safe Url"), unique=True, blank=True, null=True, max_length=100
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.product.name[:10]}-{uuid.uuid4()}")[:50] + "-videos"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name}"


class ProductTag(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"

class ProductColor(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"

class ProductMaterial(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"

        
class ProductPrice(models.Model):
    currency = models.CharField(_("Currency"), max_length=6)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    min_price = models.DecimalField(_("Min Price"), decimal_places=2, max_digits=12)
    max_price = models.DecimalField(_("Max Price"), decimal_places=2, max_digits=12)

    def save(self, *args, **kwargs):
        if not (self.product.currency or self.product.price):
            self.product.currency = self.currency
            self.product.price = self.min_price
            # self.product.save(update_fields=['currency', 'price'])
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.currency}"
        
class ProductReview(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    business = models.ForeignKey(to=ClientProfile, on_delete=models.CASCADE)
    content = models.TextField(_("Review Context"), blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"


#======================================= Product =======================================


#======================================= Order =======================================

class Order(models.Model):
    order_statuses = (
        ("PENDING", "PENDING"),
        ("VIEWED BY SUPPLER", "VIEWED BY SUPPLER"),
        ("ACCEPTED BY SUPPLER", "ACCEPTED BY SUPPLER"),
        ("IN DELIVERY", "IN DELIVERY"),
        ("DELIVERED", "DELIVERED"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),
    )
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    business = models.ForeignKey(to=ClientProfile, on_delete=models.CASCADE)
    status = models.CharField(_("Order Status"), max_length=256, choices=order_statuses, default="PENDING")
    currency = models.CharField(_("Currency"), max_length=6)
    agreed_price = models.DecimalField(_("Agreed Price"), decimal_places=2, max_digits=12)
    paid_price = models.DecimalField(_("Agreed Price"), decimal_places=2, max_digits=12)
    is_complete = models.BooleanField(_("Completed"), default=False)
    accepted_on = models.DateField(_("Accepted on"), blank=True, null=True)
    delivery_data = models.DateField(_("Delivery Date"), blank=True, null=True) 
    created_on = models.DateField(_("Created on"), default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.business}"

#======================================= Order =======================================


class Service(models.Model):
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=13)
    currency = models.CharField(_("Currency"), max_length=7)
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

class ServiceImage(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_("Service Image"),
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
        self.slug = f"{slugify(self.service.name)}-{uuid.uuid4()}"[:50]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.service.name}"


class ServiceTag(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
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
        return f"{self.service.name}"

        
# SIGNALS
@receiver(post_save, sender=Product)
def on_product_save(sender, instance, **kwargs):
    product_sub_category = instance.sub_category
    # category product count increases
    product_sub_category.category.product_count += 1
    product_sub_category.category.save(update_fields=['product_count'])


@receiver(post_delete, sender=Product)
def delete_product(sender, instance, *args, **kwargs):
    images = ProductImage.objects.filter(product=instance)
    for image in images:
        image.delete()

    videos = ProductVideo.objects.filter(product=instance)
    for video in videos:
        video.delete()

    product_sub_category = instance.sub_category
    # category product count decreases
    product_sub_category.category.product_count -= 1
    product_sub_category.category.save(update_fields=['product_count'])


@receiver(post_delete, sender=Store)
def delete_store(sender, instance, *args, **kwargs):
    if instance.image and instance.image != "test/django.png":
        instance.image.delete()
