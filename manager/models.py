from email.policy import default
from pyexpat import model
from random import choices
from re import T
from statistics import mode
import string
from weakref import proxy
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import os
import uuid
import json
import buyer

# from apps
from supplier.models import Store, Product
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
    country = models.CharField(_("Country"), max_length=256)
    city = models.CharField(_("City"), max_length=256)
    view = models.CharField(_("View"), max_length=256)
    request_method = models.CharField(_("Request Method"), max_length=256)
    device = models.CharField(_("Device"), max_length=256)
    user_os = models.CharField(_("User Os"), max_length=256)
    created_on = models.DateField(_("Created on"), default=timezone.now)


# utility functions
def get_chat_file_path(instance):
    ext = ".json"
    filename = instance.roomname
    path = os.path.join(f"{settings.CHATROOMFILES_DIR}/{filename}{ext}")
    return path


class Chatroom(models.Model):
    roomname = models.CharField(_("Chatroom Name"), max_length=256, unique=True)
    user = models.ForeignKey(
        Authmodels.User,
        on_delete=models.CASCADE,
    )
    support = models.ForeignKey(
        Authmodels.SupportProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    chatfilepath = models.CharField(
        _("Chat filepath"),
        max_length=256,
        blank=True,
        null=True,
    )
    is_closed = models.BooleanField(_("Chat Closed"), default=False)
    is_handled = models.BooleanField(_("Chat handled"), default=False)
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def save(self, *args, **kwargs):
        self.chatfilepath = get_chat_file_path(self)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Chatroom)
def create_Chat_file(sender, instance, **kwargs):
    try:
        with open(f"{instance.chatfilepath}", "w") as file:
            json.dump([], file)
    except FileNotFoundError:
        os.mkdir(f"{settings.CHATROOMFILES_DIR}")
        with open(f"{instance.chatfilepath}", "w") as file:
            json.dump([], file)

class Promotion(models.Model):
    promotion_types = (
        ("BANNER", "BANNER"),
        ("PRODUCTS", "PRODUCTS"),
        ("SUPPLIERS", "SUPPLIERS"),
        ("BUYERS", "BUYERS"),
        ("SHOWROOWS", "SHOWROOWS"),
    )

    name = models.CharField(_("Name"), max_length=256)
    description = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=get_file_path,
        blank=True,
        null=True
    )
    type = models.CharField(_("Type"), max_length=256, choices=promotion_types)
    created_on = models.DateField(_("Created on"), default=timezone.now)

    showroom = models.ForeignKey(to=Showroom, on_delete=models.CASCADE, blank=True, null=True)

    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank=True,
        null=True,
    )

    has_image = models.BooleanField(_("Has Banner Image"), default=False)
    
    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}-{uuid.uuid4()}"[:50]

        self.name = self.name

        if self.image:
            self.has_image = True

        super().save(*args, **kwargs)


class PlatformPrice(models.Model):
    advertising_price = models.DecimalField(
        _("Advertising Price"), decimal_places=2, max_digits=12, default=0.0
    )