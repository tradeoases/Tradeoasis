from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponse
from django.db.models import Q
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Count

import string
import uuid
import json

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


from supplier import tasks as SupplierTask
from auth_app import tasks as AuthTask
from manager import tasks as ManagerTask

from auth_app.tokens import appTokenGenerator

from auth_app import models as AuthModels
from supplier import models as SupplierModels
from buyer import models as BuyerModels
from manager import models as ManagerModels
from payment import models as PaymentModels

from manager import forms as ManagerForms
from auth_app import forms as AuthForms

from app_admin.mixins import SupportOnlyAccessMixin

from django.utils.translation import get_language
from googletrans import Translator
from django.conf import settings

translator = Translator()


class AdminDashboardView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/index.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard")
        context_data["active_tab"] = "Home"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Total Suppliers"),
                    "description": _("Total Supplier Count"),
                    "count": AuthModels.Supplier.supplier.all().count(),
                },
                {
                    "name": _("Total Buyers"),
                    "description": _("Total Buyer Count"),
                    "count": AuthModels.Buyer.buyer.all().count(),
                },
                {
                    "name": _("Total Product"),
                    "description": _("Total Product Count"),
                    "count": SupplierModels.Product.objects.all().count(),
                },
                {
                    "name": _("Total Showrooms"),
                    "description": _("Showroom Count"),
                    "count": ManagerModels.Showroom.objects.all().count(),
                },
                {
                    "name": _("Total Stores"),
                    "description": _("Total Store Count"),
                    "count": ManagerModels.Store.objects.all().count(),
                },
                {
                    "name": _("Total Memberships"),
                    "description": _("Memberships"),
                    "count": PaymentModels.Membership.objects.all().count(),
                },
                {
                    "name": _("Total Contracts"),
                    "description": _("Contract Created"),
                    "count": PaymentModels.Contract.objects.all().count(),
                },
            ],
        }

        context_data["user_group"] = [
            obj
            for obj in AuthModels.User.objects.values("account_type")
            .annotate(dcount=Count("account_type"))
            .order_by()
        ]

        context_data["top_suppliers"] = {
            "context_name": "top-suppliers",
            "results": AuthModels.Supplier.supplier.all()[:4],
        }
        context_data["recent_payments"] = {
            "context_name": "recent-payments",
            "results": PaymentModels.Membership.objects.all().order_by("-id")[:4],
        }
        return context_data


class AdminClientsView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/clients.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard")
        context_data["active_tab"] = "Clients"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Total Suppliers"),
                    "description": _("Total Supplier Count"),
                    "count": AuthModels.Supplier.supplier.all().count(),
                },
                {
                    "name": _("Total Buyers"),
                    "description": _("Total Buyer Count"),
                    "count": AuthModels.Buyer.buyer.all().count(),
                },
                {
                    "name": _("Total Product"),
                    "description": _("Total Product Count"),
                    "count": SupplierModels.Product.objects.all().count(),
                },
                {
                    "name": _("Total Contracts"),
                    "description": _("Contract Created"),
                    "count": PaymentModels.Contract.objects.all().count(),
                },
            ],
        }

        context_data["top_suppliers"] = {
            "context_name": "top-suppliers",
            "results": AuthModels.Supplier.supplier.all()[:6],
        }
        context_data["top_buyers"] = {
            "context_name": "top-buyers",
            "results": AuthModels.Buyer.buyer.all()[:6],
        }
        return context_data


class AdminManagersView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/manager.html"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Clients")
        context_data["active_tab"] = "Manager"
        context_data["statistics"] = {
            "context_name": "statistics",
            "results": [
                {
                    "name": _("Total Showrooms"),
                    "description": _("Showroom Count"),
                    "count": ManagerModels.Showroom.objects.all().count(),
                },
                {
                    "name": _("Total Stores"),
                    "description": _("Total Store Count"),
                    "count": ManagerModels.Store.objects.all().count(),
                },
                {
                    "name": _("Total Memberships"),
                    "description": _("Memberships"),
                    "count": PaymentModels.Membership.objects.all().count(),
                },
                {
                    "name": _("Total Services"),
                    "description": _("Total Services Count"),
                    "count": ManagerModels.Service.objects.all().count(),
                },
            ],
        }
        return context_data


class ServiceCreateView(SupportOnlyAccessMixin, CreateView):
    template_name = "app_admin/service_create.html"
    model = ManagerModels.Service
    fields = ["name", "description"]

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not (name and description):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("app_admin:service-create"))

        service = ManagerModels.Service.objects.create(
            name=request.POST.get("name"), description=request.POST.get("description")
        )

        service_image = ManagerModels.ServiceImage.objects.create(
            service = service,
            image = request.FILES.get("image")
        )

        if not service:
            messages.add_message(request, messages.ERROR, _("Invalid Data Entered."))
            return redirect(reverse("app_admin:service-create"))

        fields = ("name", "description")
        instance = service

        ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)

        messages.add_message(
            request, messages.SUCCESS, _(f"Service ({name}) created successfully.")
        )
        return redirect(reverse("app_admin:service-create"))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["view_name"] = _("Admin Dashboard - Manager")
        context_data["active_tab"] = "Manager"
        return context_data


class ShowroomCreateView(SupportOnlyAccessMixin, CreateView):
    template_name = "app_admin/showroom_create.html"
    model = ManagerModels.Showroom
    fields = ["name", "location", "image"]

    def post(self, request):
        name = request.POST.get("name")
        image = request.FILES.get("image")

        if not (name and image):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("app_admin:showroom-create"))

        showroom = ManagerModels.Showroom.objects.create(name=name, image=image)

        fields = ("name",)
        instance = showroom

        ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)

        if not showroom:
            messages.add_message(
                request, messages.ERROR, _("Error Occurred. Try Again")
            )
            return redirect(reverse("app_admin:showroom-create"))

        messages.add_message(
            request, messages.SUCCESS, _(f"Service ({name}) created successfully.")
        )
        return redirect(reverse("app_admin:showroom-create"))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["view_name"] = _("Admin Dashboard - Manager")
        context_data["active_tab"] = "Manager"
        return context_data


class CategoryCreateView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/productcategorycreate.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Clients")
        context_data["active_tab"] = "Manager"

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        name = request.POST.get("category-name")
        image = request.FILES.get("category-image")

        category = SupplierModels.ProductCategory.objects.filter(name=name)
        if category.exists():
            messages.add_message(
                request, messages.ERROR, _(f"Category({name}) already exists.")
            )
            return redirect(reverse("app_admin:category-create"))

        category = SupplierModels.ProductCategory.objects.create(name=name, image=image)
        fields = ("name",)
        instance = category
        
        ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)

        # create sub categories if any
        sub_category_len = len(request.FILES) - 1
        for i in range(1, sub_category_len + 1):
            sub_cat_name = request.POST.get(f"subcategory-{i}")
            sub_cat_image = request.FILES.get(f"sub-category-image-{i}")

            if SupplierModels.ProductSubCategory.objects.filter(
                name=sub_cat_name
            ).exists():
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(f"Sub category ({sub_cat_name}) already exists."),
                )
                continue

            sub_categgory = SupplierModels.ProductSubCategory.objects.create(
                name=sub_cat_name, image=sub_cat_image, category=category
            )

            fields = ("name",)
            instance = sub_categgory
            
            ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)


        messages.add_message(
            request,
            messages.SUCCESS,
            _("Category ({}) created successfully.").format(name),
        )
        return redirect(reverse("app_admin:category-create"))


class SubCategoryCreateView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/productsubcategorycreate.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Clients")
        context_data["active_tab"] = "Manager"
        context_data["categories"] = SupplierModels.ProductCategory.objects.all()

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        name = request.POST.get("category-name")

        category = SupplierModels.ProductCategory.objects.filter(name=name).first()

        # create sub categories if any
        sub_category_len = len(request.FILES) - 1
        for i in range(1, sub_category_len + 1):
            sub_cat_name = request.POST.get(f"subcategory-{i}")
            sub_cat_image = request.FILES.get(f"sub-category-image-{i}")

            if SupplierModels.ProductSubCategory.objects.filter(
                name=sub_cat_name
            ).exists():
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(f"Sub category ({sub_cat_name}) already exists."),
                )
                continue

            sub_categgory = SupplierModels.ProductSubCategory.objects.create(
                name=sub_cat_name, image=sub_cat_image, category=category
            )

            fields = ("name",)
            instance = sub_categgory

            ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Subcategories created successfully.").format(name),
        )
        return redirect(reverse("app_admin:subcategory-create"))


def get_last_chatroom_msg(chatroom):
    with open(chatroom.chatfilepath, "r") as file:
        current_data = json.load(file)
        return current_data[-1]


class AdminDiscussionsView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/support/index.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        context_data["chatrooms"] = {
            "context_name": "chatrooms",
            "results": [
                {"chatroom": chatroom, "last_message": get_last_chatroom_msg(chatroom)}
                for chatroom in ManagerModels.Chatroom.objects.filter(is_handled=False)
            ],
        }

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())


class AdminChatView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/support/chat.html"

    def get(self, request, roomname):
        context_data = dict()

        context_data["room_name"] = roomname
        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        context_data["chatrooms"] = {
            "context_name": "chatrooms",
            "results": [
                {"chatroom": chatroom, "last_message": get_last_chatroom_msg(chatroom)}
                for chatroom in ManagerModels.Chatroom.objects.filter(is_handled=False)
            ],
        }

        selected_chatroom = ManagerModels.Chatroom.objects.filter(roomname=roomname)
        if not selected_chatroom:
            return redirect(reverse("app_admin:discussions"))

        context_data["selected_chatroom"] = selected_chatroom.first()

        return render(request, self.template_name, context=context_data)


class AdminCommunityView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/support/community.html"

    def get_context_data(self):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"

        context_data["discussions"] = ManagerModels.Discussion.objects.all().order_by(
            "-id"
        )

        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())


class AdminCommunityChatView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/support/discussion.html"

    def get_context_data(self, slug):
        context_data = dict()

        context_data["view_name"] = _("Admin Dashboard - Support")
        context_data["active_tab"] = "Support"
        context_data["discussions"] = ManagerModels.Discussion.objects.all().order_by(
            "-id"
        )

        discussion = ManagerModels.Discussion.objects.filter(slug=slug).first()
        context_data["discussion"] = discussion
        context_data["replies"] = ManagerModels.DiscussionReply.objects.filter(
            discussion=discussion
        )

        return context_data

    def get(self, request, slug):
        return render(request, self.template_name, context=self.get_context_data(slug))

    def post(self, request, slug):
        description = request.POST.get("description")
        discussion = ManagerModels.Discussion.objects.filter(slug=slug).first()

        discussion_reply = ManagerModels.DiscussionReply.objects.create(
            description=description, user=request.user, discussion=discussion
        )

        fields = ("description",)
        instance = discussion_reply

        ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)

        return redirect(
            reverse("app_admin:community-chat", kwargs={"slug": discussion.slug})
        )


class ContactClient(SupportOnlyAccessMixin, View):
    template_name = "app_admin/create_mail.html"

    def get(self, request, slug):

        # client profile slug sent
        user = AuthModels.ClientProfile.objects.filter(slug=slug).first().user

        # get user
        context_data = {
            "user": user,
            "view_name": "Client Contact",
            "slug": slug,
            "active_tab": "Manager",
        }

        return render(request, self.template_name, context=context_data)

    def post(self, request, slug):
        name = request.POST.get("client-name")
        email = request.POST.get("client-email")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        # send email

        email_body = render_to_string(
            "email_message.html",
            {
                "name": name,
                "email": email,
                "description": description,
            },
        )
        email = EmailMessage(
            subject,
            email_body,
            request.user.email,
            [
                email,
            ],
        )
        email.send(fail_silently=False)

        # save a copy
        return redirect(reverse("app_admin:clients"))


class ProfileView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/profile.html"

    def get(self, request):

        # get user
        context_data = {
            "view_name": "Admin Profile",
            "active_tab": "Manager",
        }

        return render(request, self.template_name, context=context_data)


class EditProfileView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/editProfile.html"

    def get(self, request):
        # get user
        context_data = {
            "view_name": "Admin Profile",
            "active_tab": "Manager",
        }

        return render(request, self.template_name, context=context_data)

    def post(self, request):
        user = AuthModels.User.objects.filter(id=request.user.id).first()
        try:
            if request.POST.get("username"):
                user.first_name = request.POST.get("first_name")
            if request.POST.get("username"):
                user.last_name = request.POST.get("last_name")
            if request.POST.get("username"):
                user.username = request.POST.get("username")
            if request.POST.get("username"):
                user.email = request.POST.get("email")

            user.save()
            messages.add_message(
                request, messages.SUCCESS, _("Account Edited Successfully")
            )
            return redirect(reverse("app_admin:profile"))
        except:
            messages.add_message(
                request, messages.ERROR, _("An Error occurred. Please Try Again")
            )
            return redirect(reverse("app_admin:editprofile"))


class CreateSupportView(SupportOnlyAccessMixin, View):
    template_name = "app_admin/createProfile.html"

    def get(self, request):
        # get user
        context_data = {
            "view_name": "Admin Profile",
            "active_tab": "Manager",
        }

        return render(request, self.template_name, context=context_data)

    def post(self, request):
        if not (
            request.POST.get("username")
            and request.POST.get("email")
            and request.POST.get("password")
            and request.POST.get("confirm-password")
        ):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("app_admin:createsupport"))

        if AuthModels.User.objects.filter(username=request.POST.get("username")):
            messages.add_message(request, messages.ERROR, _("Username not available."))
            return redirect(reverse("app_admin:createsupport"))

        if request.POST.get("confirm-password") != request.POST.get("password"):
            messages.add_message(request, messages.ERROR, _("Password mismatch."))
            return redirect(reverse("app_admin:createsupport"))

        user = AuthModels.User.objects.create_user(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
            account_type="SUPPORT",
        )

        AuthModels.SupportProfile.objects.create(user=user)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = appTokenGenerator.make_token(user)
        domain = get_current_site(request).domain
        link = reverse("app_admin:activate", kwargs={"uidb64": uidb64, "token": token})

        activate_url = f"http://{domain}{link}"

        email_body = render_to_string(
            "email_message.html",
            {
                "name": user.username,
                "email": user.email,
                "review": "{} \n {} \n Please edit your account details and set a desired password after activating your account.".format(
                    _("Your activation link is"), activate_url
                ),
            },
        )
        email = EmailMessage(
            _("Activate Foroden Activation"),
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [
                user.email,
            ],
        )
        email.send(fail_silently=False)

        messages.add_message(
            request,
            messages.SUCCESS,
            _(
                "Account Created Successfully.  A verification link was sent user's email."
            ),
        )
        return redirect(reverse("app_admin:profile"))


class VerficationView(View):
    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = AuthModels.User.objects.filter(pk=uid).first()

        if user and appTokenGenerator.check_token(user, token):
            user.is_email_activated = True
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            # to set password
            return redirect(reverse("app_admin:profile"))
        else:
            return HttpResponseNotFound(_("Bad Request"))


# promotion
class AdminPromotionsView(View):
    template_name = "app_admin/promotion_list.html"

    def get(self, request):
        context_data = {
            "view_name": "Admin Dashboard",
            "active_tab": "Promotions",
            "text_promotions" : ManagerModels.Promotion.objects.filter(has_image=False),
            "banner_promotions" : ManagerModels.Promotion.objects.filter(has_image=True),
        }

        return render(request, self.template_name, context=context_data)

class AdminPromotionsCreateView(View):
    template_name = "app_admin/promotion_create.html"

    def get(self, request):
        context_data = {
            "view_name": "Admin Dashboard",
            "active_tab": "Promotions",
            "showrooms" : ManagerModels.Showroom.objects.all(),
            "choices" : ["BANNER", "PRODUCTS", "SUPPLIERS", "BUYERS", "SHOWROOWS"]
        }

        return render(request, self.template_name, context=context_data)

    def post(self, request):
        name = request.POST.get("name")
        promotion_types = request.POST.get("promotion_types")
        showrooms = request.POST.get("showrooms")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        
        if not image and not description:
            messages.add_message(request, messages.ERROR, _("Offer description for text promotions"))
            return redirect(reverse("app_admin:promotions-create"))
        elif promotion_types != "SHOWROOWS":

            promotion = ManagerModels.Promotion.objects.create(
                name = name,
                type = promotion_types,
                description = description,
                image = image if image else None,
            )
            if not promotion:
                messages.add_message(request, messages.ERROR, _("An Error occured. Try Again."))
                return redirect(reverse("app_admin:promotions-create"))

        elif promotion_types == "SHOWROOWS":

            promotion = ManagerModels.Promotion.objects.create(
                name = name,
                type = promotion_types,
                description = description,
                image = image if image else None,
                showroom = ManagerModels.Showroom.objects.filter(slug=showrooms).first()
            )
            if not promotion:
                messages.add_message(request, messages.ERROR, _("An Error occured. Try Again."))
                return redirect(reverse("app_admin:promotions-create"))

        
        fields = ("name", "description",)
        instance = promotion

        ManagerTask.make_model_translations.delay(fields, instance.pk, instance.__class__.__name__)

        messages.add_message(request, messages.SUCCESS, _("Promotion Created Successfully."))
        return redirect(reverse("app_admin:promotions-create"))