from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser


# Create your models here.
# USER MANAGER
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_customer = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_customer = False
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# USER MODEL
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_email_activated = models.BooleanField(default=False)

    Role = (
        ("ADMIN", "Admin"),
        ("SUPPORT", "Support"),
        ("SUPPLIER", "Supplier"),
        ("BUYER", "Buyer"),
        ("CUSTOMER", "Customer"),
    )
    account_type = models.CharField(max_length=225, choices=Role, default='CUSTOMER')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.last_name + ' - ' + self.last_name + ' - ' + self.email


# SYSTEM MODELS START HERE
class BusinessProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    tin_number = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=255, null=True, blank=True)
    # image
    slogan = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=355, null=True, blank=True)
    store_url = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class ShowRoom(models.Model):
    showroom_location = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(max_length=355, null=True, blank=True)

    # image

    def __str__(self):
        return self.showroom_location


class AuditTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.TextField(max_length=355, null=True, blank=True)

    def __str__(self):
        return self.user.email
