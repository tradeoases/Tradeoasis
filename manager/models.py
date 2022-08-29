import string
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os
import uuid

# from apps
from supplier.models import Store
from auth_app import models as Authmodels


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)


class Location(models.Model):
    name = models.CharField(_("Country or City"), max_length=256)
    created_on = models.DateField(_("Created on"), default=timezone.now)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}-{uuid.uuid4()}"[:50]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class Service(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(
        _("Description"),
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}-{uuid.uuid4()}"[:50]

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
        self.slug = f"{slugify(self.service.name)}-{uuid.uuid4()}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.service.name}"


class Showroom(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    store = models.ManyToManyField(to=Store, related_name="store", default=None)
    location = models.ForeignKey(
        to=Location, on_delete=models.CASCADE, blank=True, null=True
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
        default="test/django.png",
    )
    visits = models.IntegerField(_("Number of visits"), default=0)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}-{uuid.uuid4()}"[:50]

        self.name = self.name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class Discussion(models.Model):
    class Meta:
        ordering = ["-id"]

    subject = models.CharField(_("Subject"), max_length=256)
    description = models.TextField(_("Description"))
    user = models.ForeignKey(to=Authmodels.User, on_delete=models.CASCADE)
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.subject)}-{uuid.uuid4()}"[:50]

        self.name = self.subject

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.subject}"


class DiscussionReply(models.Model):

    discussion = models.ForeignKey(to=Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Authmodels.User, on_delete=models.CASCADE)
    description = models.TextField(_("Description"))
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def __str__(self) -> str:
        return f"{self.discussion.subject}"


class UserRequest(models.Model):
    country = models.CharField(_('Country'), max_length=256)
    city = models.CharField(_('City'), max_length=256)
    view = models.CharField(_('View'), max_length=256)
    request_method = models.CharField(_('Request Method'), max_length=256)
    device = models.CharField(_('Device'), max_length=256)
    user_os = models.CharField(_('User Os'), max_length=256)
    created_on = models.DateField(_("Created on"), default=timezone.now)
