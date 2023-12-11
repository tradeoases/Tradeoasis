from django.urls import path, include

from api.vendor.controllers.business_profile import get_business_profile, delete_business_profile, \
   update_business_profile

app_name = 'vendor'

urlpatterns = [
    path('', include('api.shared.urls')),
    path('detail_business_profile/<str:pk>/', get_business_profile, name='business_profile'),
    path('business_profile/delete/<str:pk>/', delete_business_profile, name='business_profile_delete'),
    path('update_business_profile/<str:pk>/', update_business_profile, name='update_business_profile'),

]
