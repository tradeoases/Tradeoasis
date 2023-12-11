from django.urls import path, include
from api.vendor.controllers.business_profile import get_business_profile

app_name = 'buyer'

urlpatterns = [
    path('', include('api.shared.urls')),
    path('detail_business_profile/<str:pk>/', get_business_profile, name='business_profile'),
]
