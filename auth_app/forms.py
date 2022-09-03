from django.forms import ModelForm

from auth_app import models as AuthModels

from allauth.socialaccount.forms import SignupForm
from django import forms


class UserProfileFormManager(ModelForm):
    class Meta:
        model = AuthModels.ClientProfile
        fields = "__all__"


class UserFormManager(ModelForm):
    class Meta:
        model = AuthModels.User
        fields = "__all__"

 
class CustomSignupForm(SignupForm):
    CHOICES=[
        ("SUPPLIER", "Supplier"),
        ("BUYER", "Buyer")
    ]
    account_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.account_type = self.cleaned_data['account_type']
        user.active = True
        user.is_email_activated = True
        user.save()
        return user