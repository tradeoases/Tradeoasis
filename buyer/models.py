# django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# apps
from supplier.models import Product

# apps
from auth_app.models import Buyer


class WishList(models.Model):
    buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    is_handled = models.BooleanField(_("interest handled"), default=False)
    viewed_by_supplied = models.BooleanField(_("Viewed by supplier"), default=False)
    created_on = models.DateField(_("Created on"), default=timezone.now)

    def __str__(self) -> str:
        return f"Buyer: {self.buyer.username} - Product: {self.product.name}"


# SIGNALS
@receiver(post_save, sender=WishList)
def on_wishlist_save(sender, instance, **kwargs):
    # send supplier email
    pass
