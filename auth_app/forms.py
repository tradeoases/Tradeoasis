from django.forms import ModelForm

from auth_app import models as AuthModels


class UserProfileFormManager(ModelForm):
    class Meta:
        model = AuthModels.ClientProfile
        fields = "__all__"


class UserFormManager(ModelForm):
    class Meta:
        model = AuthModels.User
        fields = "__all__"
