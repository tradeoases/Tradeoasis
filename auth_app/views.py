from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponseNotFound

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from auth_app import models as AuthModels

from auth_app.forms import UserProfileFormManager

from auth_app.tasks import send_account_activation_email_task
from auth_app.tokens import appTokenGenerator

class LoginView(View):
    template_name = 'auth_app/signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('manager:home'))
        context_data = {
            "view_name": _("Sign In")
        }

        return render(request, self.template_name, context=context_data)

    def post(self, request):
        if not (request.POST.get('username') and request.POST.get('password')):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("auth_app:login"))

        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if not user:
            messages.add_message(request, messages.ERROR, _("Account not found. Try Again."))
            return redirect(reverse("auth_app:login"))

        if not user.is_email_activated:
            messages.add_message(request, messages.ERROR, _("Please Activate your Email"))
            return redirect(reverse("auth_app:login"))

        login(request, user)
        if request.GET.get('next'):
            return redirect(reverse(request.GET.get('next')))
        return redirect(reverse('manager:home'))


class SignUpView(View):
    template_name = 'auth_app/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('manager:home'))

        context_data = {
            "view_name": _("Sign Up")
        }

        return render(request, self.template_name, context=context_data)


    def post(self, request):
        if not (request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('confirm-password')):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("auth_app:signup"))

        if AuthModels.User.objects.filter(username=request.POST.get('username')):
            messages.add_message(request, messages.ERROR, _("Please Fill all fields."))
            return redirect(reverse("auth_app:signup"))

        if request.POST.get('confirm-password') != request.POST.get('password'):
            messages.add_message(request, messages.ERROR, _("Password mismatch."))
            return redirect(reverse("auth_app:signup"))

        if self.request.GET.get('supplier'):
            account_type = 'Supplier'
            UserModel = AuthModels.Supplier
        else:
            account_type = 'Buyer'
            UserModel = AuthModels.Buyer

        user = UserModel.objects.create_user(first_name = request.POST.get('first_name'), last_name = request.POST.get('last_name'), username = request.POST.get('username'), email = request.POST.get('email'), password = request.POST.get('password'), account_type=account_type)


        # send activation link
        # send_account_activation_email_task.delay(user.username, user.email, "Activate Foroden Activation")

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = appTokenGenerator.make_token(user)
        domain = get_current_site(request).domain
        link = reverse('auth_app:activate', kwargs={"uidb64": uidb64, "token": token})

        activate_url = f'http://{domain}{link}'

        email_body = render_to_string('email_message.html', {
            'name': user.username,
            'email': user.email,
            'review': "{} \n {}".format(_("Your activation link is"), activate_url)
        })
        email = EmailMessage(
            _('Activate Foroden Activation'), email_body,
            settings.DEFAULT_FROM_EMAIL, [user.email, ],
        )
        email.send(fail_silently=False)

        messages.add_message(request, messages.SUCCESS, _("Account Created Successfully. Please check your email for a verfication link."))
        return redirect(reverse("auth_app:login"))

class VerficationView(View):
    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = AuthModels.User.objects.filter(pk=uid).first()

        if user and appTokenGenerator.check_token(user, token):
            user.is_email_activated = True
            user.save()
            login(request, user)
            # to dashboard
            return redirect(reverse("auth_app:business"))
        else:
            return HttpResponseNotFound(_("Bad Request"))


def LogoutView(request):
    logout(request)
    return redirect(reverse('auth_app:login'))


class BusinessProfileView(View):
    template_name = 'auth_app/business_infor.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('auth_app:login'))

        if AuthModels.ClientProfile.objects.filter(user=request.user):
            return redirect(reverse('manager:home'))

        context_data = {
            "view_name": _("Business Profile")
        }

        return render(request, self.template_name, context=context_data)

    def post(self, request):
        if not (request.POST.get('business_name') and request.POST.get('business_description') and request.POST.get('country') and request.POST.get('city') and request.POST.get('country_code') and request.POST.get('mobile_user')):
            messages.add_message(request, messages.ERROR, _("Please Fill all reqiured fields."))
            return redirect(reverse("auth_app:business"))


        try:
            AuthModels.ClientProfile.objects.create(
                user = request.user,
                business_name = request.POST.get('business_name'),
                business_description = request.POST.get('business_description'),
                country = request.POST.get('country'),
                city = request.POST.get('city'),
                country_code = request.POST.get('country_code'),
                mobile_user = request.POST.get('mobile_user'),
                vat_number = request.POST.get('vat_number', None),
                legal_etity_identifier = request.POST.get('legal_etity_identifier', None),
                website = request.POST.get('website', None)
            )
        except:
            messages.add_message(request, messages.ERROR, _("An Error Occured. Try Again."))
            return redirect(reverse("auth_app:business"))
