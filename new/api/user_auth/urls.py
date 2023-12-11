from django.urls import path

from api.user_auth.controllers.authenticate import MyTokenObtainPairView, get_user_profile

urlpatterns = [
    #     AUTHENTICATE
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('user_profile/', get_user_profile, name='user_profile'),
    ]